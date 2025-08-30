
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Callable, Any
import math, random, enum

class Type(enum.IntEnum):
    NORMAL=0; FIGHTING=1; FLYING=2; POISON=3; GROUND=4; ROCK=5; BUG=6; GHOST=7; STEEL=8; FAIRY=9
    FIRE=10; WATER=11; GRASS=12; ELECTRIC=13; PSYCHIC=14; ICE=15; DRAGON=16; DARK=17

EFFECT_DOUBLE_WEAK   = 0xF0
EFFECT_WEAK          = 0x78
EFFECT_NEUTRAL       = 0x28
EFFECT_RESIST        = 0x1E
EFFECT_DOUBLE_RESIST = 0x0F
EFFECT_IMMUNE        = 0x00

class Category(enum.IntEnum):
    PHYSICAL=0; SPECIAL=1; STATUS=2

class Stat(enum.IntEnum):
    HP=0; ATTACK=1; DEFENSE=2; SPEED=3; SP_ATTACK=4; SP_DEFENSE=5
    ACCURACY=6; EVASION=7

class Target(enum.IntEnum):
    DEFENDER=0; ATTACKER=1; A_PARTNER=2; D_PARTNER=3

class Ability(enum.IntEnum):
    NONE=0; STURDY=5; DAMP=6; WONDER_GUARD=25; LEVITATE=26

class Weather(enum.IntEnum):
    CLEAR=0; RAIN=1; SUN=2; SAND=3; HAIL=4

class MajorStatus(enum.IntFlag):
    NONE=0
    SLEEP=0x07
    POISON=0x08
    BURN=0x10
    FREEZE=0x20
    PARALYZE=0x40
    BAD_POISON=0x80
    MAJOR_MASK=0xFF

def _effectiveness(attack: Type, defend: Type) -> float:
    chart = {
        Type.NORMAL:  {Type.ROCK:0.5, Type.STEEL:0.5, Type.GHOST:0.0},
        Type.FIGHTING:{Type.NORMAL:2, Type.ROCK:2, Type.STEEL:2, Type.ICE:2, Type.DARK:2, Type.FLYING:0.5, Type.POISON:0.5, Type.BUG:0.5, Type.PSYCHIC:0.5, Type.FAIRY:0.5, Type.GHOST:0.0},
        Type.FLYING:  {Type.FIGHTING:2, Type.BUG:2, Type.GRASS:2, Type.ROCK:0.5, Type.STEEL:0.5, Type.ELECTRIC:0.5},
        Type.POISON:  {Type.GRASS:2, Type.FAIRY:2, Type.POISON:0.5, Type.GROUND:0.5, Type.ROCK:0.5, Type.GHOST:0.5, Type.STEEL:0.0},
        Type.GROUND:  {Type.FIRE:2, Type.ELECTRIC:2, Type.POISON:2, Type.ROCK:2, Type.STEEL:2, Type.BUG:0.5, Type.GRASS:0.5, Type.FLYING:0.0},
        Type.ROCK:    {Type.FIRE:2, Type.ICE:2, Type.FLYING:2, Type.BUG:2, Type.FIGHTING:0.5, Type.GROUND:0.5, Type.STEEL:0.5},
        Type.BUG:     {Type.GRASS:2, Type.PSYCHIC:2, Type.DARK:2, Type.FIGHTING:0.5, Type.FLYING:0.5, Type.POISON:0.5, Type.GHOST:0.5, Type.STEEL:0.5, Type.FIRE:0.5, Type.FAIRY:0.5},
        Type.GHOST:   {Type.PSYCHIC:2, Type.GHOST:2, Type.NORMAL:0.0, Type.DARK:0.5},
        Type.STEEL:   {Type.ROCK:2, Type.ICE:2, Type.FAIRY:2, Type.STEEL:0.5, Type.FIRE:0.5, Type.WATER:0.5, Type.ELECTRIC:0.5},
        Type.FAIRY:   {Type.FIGHTING:2, Type.DRAGON:2, Type.DARK:2, Type.POISON:0.5, Type.STEEL:0.5, Type.FIRE:0.5},
        Type.FIRE:    {Type.GRASS:2, Type.ICE:2, Type.BUG:2, Type.STEEL:2, Type.FIRE:0.5, Type.WATER:0.5, Type.ROCK:0.5, Type.DRAGON:0.5},
        Type.WATER:   {Type.FIRE:2, Type.ROCK:2, Type.GROUND:2, Type.WATER:0.5, Type.GRASS:0.5, Type.DRAGON:0.5},
        Type.GRASS:   {Type.WATER:2, Type.ROCK:2, Type.GROUND:2, Type.FIRE:0.5, Type.GRASS:0.5, Type.POISON:0.5, Type.FLYING:0.5, Type.BUG:0.5, Type.DRAGON:0.5, Type.STEEL:0.5},
        Type.ELECTRIC:{Type.WATER:2, Type.FLYING:2, Type.GRASS:0.5, Type.ELECTRIC:0.5, Type.DRAGON:0.5, Type.GROUND:0.0},
        Type.PSYCHIC: {Type.FIGHTING:2, Type.POISON:2, Type.PSYCHIC:0.5, Type.STEEL:0.5, Type.DARK:0.0},
        Type.ICE:     {Type.GRASS:2, Type.GROUND:2, Type.FLYING:2, Type.DRAGON:2, Type.FIRE:0.5, Type.WATER:0.5, Type.ICE:0.5, Type.STEEL:0.5},
        Type.DRAGON:  {Type.DRAGON:2, Type.STEEL:0.5, Type.FAIRY:0.0},
        Type.DARK:    {Type.PSYCHIC:2, Type.GHOST:2, Type.FIGHTING:0.5, Type.DARK:0.5, Type.FAIRY:0.5},
    }
    return chart.get(Type(attack), {}).get(Type(defend), 1.0)

def type_effectiveness(move_type: Type, defender_types: Tuple[Type, Optional[Type]], defender_ability: Ability) -> float:
    if move_type == Type.GROUND and defender_ability == Ability.LEVITATE:
        return 0.0
    mult = _effectiveness(move_type, defender_types[0])
    if defender_types[1] is not None:
        mult *= _effectiveness(move_type, defender_types[1])
    return mult

def effect_to_byte(mult: float) -> int:
    if mult == 0.0: return EFFECT_IMMUNE
    if math.isclose(mult, 0.25): return EFFECT_DOUBLE_RESIST
    if math.isclose(mult, 0.5): return EFFECT_RESIST
    if math.isclose(mult, 1.0): return EFFECT_NEUTRAL
    if math.isclose(mult, 2.0): return EFFECT_WEAK
    if math.isclose(mult, 4.0): return EFFECT_DOUBLE_WEAK
    return EFFECT_NEUTRAL

@dataclass
class Move:
    id: int; name: str; type: Type; power: int; accuracy: int; category: int
    priority: int = 0; flags: int = 0

@dataclass
class Pokemon:
    name: str; level: int; types: Tuple[Type, Optional[Type]]; ability: Ability
    max_hp: int; hp: int; atk: int; defense: int; sp_atk: int; sp_def: int; speed: int
    status1: MajorStatus = MajorStatus.NONE
    moves: List[Move] = field(default_factory=list)
    def is_fainted(self) -> bool: return self.hp <= 0
    def hp_ratio_percent(self) -> int: return int((self.hp / self.max_hp) * 100) if self.max_hp>0 else 0

@dataclass
class Side:
    active: Pokemon; bench: List[Pokemon] = field(default_factory=list)

@dataclass
class Battle:
    attacker: Side; defender: Side; weather: Weather = Weather.CLEAR
    def count_viable(self, side: Side) -> int:
        return int(not side.active.is_fainted()) + sum(int(not p.is_fainted()) for p in side.bench)

def expected_damage(attacker: Pokemon, defender: Pokemon, move: Move, weather: Weather) -> int:
    if move.category == 2 or move.power <= 0: return 0
    mult = type_effectiveness(move.type, defender.types, defender.ability)
    if mult == 0.0: return 0
    stab = 1.5 if (move.type in attacker.types) else 1.0
    w_mult = 1.0
    if weather == Weather.RAIN and move.type == Type.WATER: w_mult = 1.5
    if weather == Weather.RAIN and move.type == Type.FIRE:  w_mult = 0.5
    if weather == Weather.SUN  and move.type == Type.FIRE:  w_mult = 1.5
    if weather == Weather.SUN  and move.type == Type.WATER: w_mult = 0.5
    if move.category == 0: atk_stat,def_stat = attacker.atk, defender.defense
    else:                   atk_stat,def_stat = attacker.sp_atk, defender.sp_def
    base = (((2 * attacker.level / 5) + 2) * move.power * (atk_stat / max(1, def_stat)) / 50) + 2
    dmg = int(base * stab * mult * w_mult)
    dmg = int(dmg * (move.accuracy / 100))
    return max(0, min(dmg, defender.hp))

def would_KO(attacker: Pokemon, defender: Pokemon, move: Move, weather: Weather) -> bool:
    return expected_damage(attacker, defender, move, weather) >= defender.hp

def damage_bonus_byte(attacker: Pokemon, defender: Pokemon, move: Move) -> int:
    return effect_to_byte(type_effectiveness(move.type, defender.types, defender.ability))

class OpCode(enum.IntEnum):
    RANDOM_LT=0x00; RANDOM_GT=0x01; RANDOM_ONE_IN_256=0x02; RANDOM_255_IN_256=0x03; ADD_VIABILITY=0x04
    J_IF_HP_LT=0x05; J_IF_HP_GT=0x06; J_IF_HP_EQ=0x07; J_IF_HP_NEQ=0x08
    J_IF_STATUS1_EQ=0x09; J_IF_STATUS1_NEQ=0x0A
    J_IF_BYTE_LT=0x11; J_IF_BYTE_GT=0x12; J_IF_BYTE_EQ=0x13; J_IF_BYTE_NEQ=0x14
    J_IF_WORD_LT=0x15; J_IF_WORD_GT=0x16; J_IF_WORD_EQ=0x17; J_IF_WORD_NEQ=0x18
    J_IF_MOVE_ID_EQ=0x19; J_IF_MOVE_ID_NEQ=0x1A
    J_IF_ATTACKER_HAS_DAMAGING=0x1F; J_IF_ATTACKER_HAS_NO_DAMAGING=0x20
    GET_TURN_COUNTER=0x21; GET_TYPE=0x22; GET_POWER_OF_CONSIDERED=0x23; GET_POWER_OF_STRONGEST=0x24
    GET_MOVE_LAST_USED=0x25; J_IF_FREEVAR_EQ=0x26; J_IF_FREEVAR_NEQ=0x27
    J_IF_MOVE_WOULD_HIT_FIRST=0x28
    GET_PERISH_COUNT=0x2A; GET_SPIKES_LAYER=0x2B; COUNT_VIABLE_ON_TEAM=0x2C; GET_MOVE_ID=0x2D
    GET_MOVE_SCRIPT_ID=0x2E; GET_ABILITY=0x2F; CALL_ASM=0x30; J_IF_DMG_BONUS_EQ=0x31
    J_IF_ANY_OR_ALL_STATS=0x32; DOES_TEETER_DANCE_WORK=0x33
    J_IF_ANY_POKEMON_HAS_STATUS=0x34; J_IF_NO_POKEMON_HAS_STATUS=0x35; GET_WEATHER=0x36
    J_IF_MOVESCRIPT_EQ=0x37; J_IF_MOVESCRIPT_NEQ=0x38
    J_IF_STAT_BUFF_LT=0x39; J_IF_STAT_BUFF_GT=0x3A; J_IF_STAT_BUFF_EQ=0x3B; J_IF_STAT_BUFF_NEQ=0x3C
    J_IF_MOVE_KO=0x3D; J_IF_MOVE_NOT_KO=0x3E
    J_IF_MOVE_IN_SET=0x3F; J_IF_MOVE_NOT_IN_SET=0x40
    CALL=0x58; JUMP=0x59; RETURN_TO_BATTLE=0x5A; J_IF_LEVELS_ARE=0x5B; J_IF_TAUNT_TURNS_NOT_ZERO=0x5C; J_IF_TAUNT_TURNS_ZERO=0x5D

from dataclasses import dataclass
from typing import Optional

@dataclass
class Instruction:
    op: OpCode
    args: tuple = ()
    label: Optional[str] = None

class Script:
    def __init__(self):
        self.instructions: List[Instruction] = []
        self.labels: Dict[str, int] = {}
    def label(self, name: str): self.labels[name]=len(self.instructions)
    def emit(self, op: OpCode, *args): self.instructions.append(Instruction(op, args))
    def jmp(self, label: str): self.emit(OpCode.JUMP, label)
    def call(self, label: str): self.emit(OpCode.CALL, label)
    def ret(self): self.emit(OpCode.RETURN_TO_BATTLE)
    def _resolve(self, label: str) -> int:
        if label not in self.labels: raise KeyError(f"Unknown label: {label}")
        return self.labels[label]

class AIVM:
    def __init__(self, battle: Battle, rng: Optional[random.Random]=None):
        self.battle=battle; self.rng=rng or random.Random()
        self.byte_reg=0; self.word_reg=0; self.free_var=0; self.turn_counter=1
        self.considered_move_index=0; self.stack=[]; self.pc=0; self.viability=[0,0,0,0]; self.running=True
    @property
    def attacker(self)->Pokemon: return self.battle.attacker.active
    @property
    def defender(self)->Pokemon: return self.battle.defender.active
    def _jump(self, script: Script, label: str): self.pc=script._resolve(label)
    def _call(self, script: Script, label: str): self.stack.append(self.pc); self.pc=script._resolve(label)
    def _ret(self): self.running=False if not self.stack else None or (self.stack and (setattr(self, "pc", self.stack.pop()) or True))
    def run(self, script: Script) -> int:
        for idx,_ in enumerate(self.attacker.moves):
            self.considered_move_index=idx; self.pc=0; self.stack.clear(); self.running=True; self.byte_reg=0; self.word_reg=0
            while self.running and self.pc < len(script.instructions):
                instr=script.instructions[self.pc]; self.pc+=1; self._exec_instr(script, instr)
        best = max(range(len(self.attacker.moves)), key=lambda i: (self.viability[i], expected_damage(self.attacker,self.defender,self.attacker.moves[i], self.battle.weather)))
        return best
    def _current_move(self)->Move: return self.attacker.moves[self.considered_move_index]
    def _has_any_damaging_move(self, mon: Pokemon)->bool: return any(m.power>0 for m in mon.moves)
    def _exec_instr(self, script: Script, instr: Instruction):
        op,args=instr.op,instr.args
        if op==OpCode.RANDOM_LT:
            threshold,label=args;  self._jump(script,label) if self.rng.randrange(256)<int(threshold) else None
        elif op==OpCode.RANDOM_GT:
            threshold,label=args;  self._jump(script,label) if self.rng.randrange(256)>int(threshold) else None
        elif op==OpCode.RANDOM_ONE_IN_256:
            (label,)=args;         self._jump(script,label) if self.rng.randrange(256)==0 else None
        elif op==OpCode.RANDOM_255_IN_256:
            (label,)=args;         self._jump(script,label) if self.rng.randrange(256)!=0 else None
        elif op==OpCode.ADD_VIABILITY:
            (val,)=args;           self.viability[self.considered_move_index]+=int(val)
        elif op==OpCode.J_IF_HP_LT:
            target,value,label=args; mon=self.defender if target==Target.DEFENDER else self.attacker
            self._jump(script,label) if mon.hp_ratio_percent()<int(value) else None
        elif op==OpCode.J_IF_HP_GT:
            target,value,label=args; mon=self.defender if target==Target.DEFENDER else self.attacker
            self._jump(script,label) if mon.hp_ratio_percent()>int(value) else None
        elif op==OpCode.J_IF_HP_EQ:
            target,value,label=args; mon=self.defender if target==Target.DEFENDER else self.attacker
            self._jump(script,label) if mon.hp_ratio_percent()==int(value) else None
        elif op==OpCode.J_IF_HP_NEQ:
            target,value,label=args; mon=self.defender if target==Target.DEFENDER else self.attacker
            self._jump(script,label) if mon.hp_ratio_percent()!=int(value) else None
        elif op==OpCode.J_IF_STATUS1_EQ:
            target,mask,label=args; mon=self.defender if target==Target.DEFENDER else self.attacker
            self._jump(script,label) if (mon.status1 & MajorStatus(mask))==MajorStatus(mask) else None
        elif op==OpCode.J_IF_STATUS1_NEQ:
            target,mask,label=args; mon=self.defender if target==Target.DEFENDER else self.attacker
            self._jump(script,label) if (mon.status1 & MajorStatus(mask))!=MajorStatus(mask) else None
        elif op==OpCode.J_IF_BYTE_LT:
            value,label=args;       self._jump(script,label) if self.byte_reg<int(value) else None
        elif op==OpCode.J_IF_BYTE_GT:
            value,label=args;       self._jump(script,label) if self.byte_reg>int(value) else None
        elif op==OpCode.J_IF_BYTE_EQ:
            value,label=args;       self._jump(script,label) if self.byte_reg==int(value) else None
        elif op==OpCode.J_IF_BYTE_NEQ:
            value,label=args;       self._jump(script,label) if self.byte_reg!=int(value) else None
        elif op==OpCode.J_IF_WORD_LT:
            value,label=args;       self._jump(script,label) if self.word_reg<int(value) else None
        elif op==OpCode.J_IF_WORD_GT:
            value,label=args;       self._jump(script,label) if self.word_reg>int(value) else None
        elif op==OpCode.J_IF_WORD_EQ:
            value,label=args;       self._jump(script,label) if self.word_reg==int(value) else None
        elif op==OpCode.J_IF_WORD_NEQ:
            value,label=args;       self._jump(script,label) if self.word_reg!=int(value) else None
        elif op==OpCode.J_IF_MOVE_ID_EQ:
            move_id,label=args;     self._jump(script,label) if self._current_move().id==int(move_id) else None
        elif op==OpCode.J_IF_MOVE_ID_NEQ:
            move_id,label=args;     self._jump(script,label) if self._current_move().id!=int(move_id) else None
        elif op==OpCode.J_IF_ATTACKER_HAS_DAMAGING:
            (label,)=args;          self._jump(script,label) if self._has_any_damaging_move(self.attacker) else None
        elif op==OpCode.J_IF_ATTACKER_HAS_NO_DAMAGING:
            (label,)=args;          self._jump(script,label) if not self._has_any_damaging_move(self.attacker) else None
        elif op==OpCode.GET_TURN_COUNTER:
            self.byte_reg=self.turn_counter
        elif op==OpCode.GET_TYPE:
            (argument,)=args
            if argument=="DEFENDER_TYPE1": self.byte_reg=int(self.defender.types[0])
            elif argument=="DEFENDER_TYPE2": self.byte_reg=int(self.defender.types[1] if self.defender.types[1] is not None else 0)
            elif argument=="ATTACKER_TYPE1": self.byte_reg=int(self.attacker.types[0])
            elif argument=="ATTACKER_TYPE2": self.byte_reg=int(self.attacker.types[1] if self.attacker.types[1] is not None else 0)
            elif argument=="MOVE": self.byte_reg=int(self._current_move().type)
            else: self.byte_reg=0
        elif op==OpCode.GET_POWER_OF_CONSIDERED:
            self.byte_reg=int(self._current_move().power)
        elif op==OpCode.GET_POWER_OF_STRONGEST:
            powers=[m.power for m in self.attacker.moves]; self.byte_reg=max(powers) if powers else 0
        elif op==OpCode.GET_MOVE_LAST_USED:
            self.byte_reg=0
        elif op==OpCode.J_IF_FREEVAR_EQ:
            value,label=args; self._jump(script,label) if self.free_var==int(value) else None
        elif op==OpCode.J_IF_FREEVAR_NEQ:
            value,label=args; self._jump(script,label) if self.free_var!=int(value) else None
        elif op==OpCode.J_IF_MOVE_WOULD_HIT_FIRST:
            priority,label=args; mv=self._current_move(); att=(mv.priority,self.attacker.speed); defp=(0,self.defender.speed)
            self._jump(script,label) if att>defp else None
        elif op==OpCode.COUNT_VIABLE_ON_TEAM:
            (who,)=args; side=self.battle.defender if who==Target.DEFENDER else self.battle.attacker; self.byte_reg=self.battle.count_viable(side)
        elif op==OpCode.GET_MOVE_ID:
            self.word_reg=self._current_move().id
        elif op==OpCode.GET_MOVE_SCRIPT_ID:
            (move_id,)=args; self.byte_reg=0
        elif op==OpCode.GET_ABILITY:
            (target,)=args; mon=self.defender if target==Target.DEFENDER else self.attacker; self.byte_reg=int(mon.ability)
        elif op==OpCode.CALL_ASM:
            pass
        elif op==OpCode.J_IF_DMG_BONUS_EQ:
            move_slot_or_zero,value,label=args; move=self._current_move() if int(move_slot_or_zero)==0 else self.attacker.moves[int(move_slot_or_zero)]
            bonus=damage_bonus_byte(self.attacker,self.defender,move)
            self._jump(script,label) if bonus==int(value) else None
        elif op in (OpCode.J_IF_ANY_OR_ALL_STATS, OpCode.DOES_TEETER_DANCE_WORK, OpCode.J_IF_MOVESCRIPT_EQ, OpCode.J_IF_MOVESCRIPT_NEQ,
                    OpCode.J_IF_STAT_BUFF_LT, OpCode.J_IF_STAT_BUFF_GT, OpCode.J_IF_STAT_BUFF_EQ, OpCode.J_IF_STAT_BUFF_NEQ,
                    OpCode.J_IF_TAUNT_TURNS_NOT_ZERO, OpCode.J_IF_TAUNT_TURNS_ZERO):
            pass
        elif op==OpCode.J_IF_ANY_POKEMON_HAS_STATUS:
            target,mask,label=args; mons=[self.attacker]+self.battle.attacker.bench if target==Target.ATTACKER else [self.defender]+self.battle.defender.bench
            self._jump(script,label) if any((m.status1 & MajorStatus(mask))==MajorStatus(mask) for m in mons) else None
        elif op==OpCode.J_IF_NO_POKEMON_HAS_STATUS:
            target,mask,label=args; mons=[self.attacker]+self.battle.attacker.bench if target==Target.ATTACKER else [self.defender]+self.battle.defender.bench
            self._jump(script,label) if all((m.status1 & MajorStatus(mask))!=MajorStatus(mask) for m in mons) else None
        elif op==OpCode.GET_WEATHER:
            self.byte_reg=int(self.battle.weather)
        elif op==OpCode.J_IF_MOVE_KO:
            (label,)=args; self._jump(script,label) if would_KO(self.attacker,self.defender,self._current_move(),self.battle.weather) else None
        elif op==OpCode.J_IF_MOVE_NOT_KO:
            (label,)=args; self._jump(script,label) if not would_KO(self.attacker,self.defender,self._current_move(),self.battle.weather) else None
        elif op==OpCode.J_IF_MOVE_IN_SET:
            target,move_id,label=args; mon=self.defender if target==Target.DEFENDER else self.attacker
            self._jump(script,label) if any(m.id==int(move_id) for m in mon.moves) else None
        elif op==OpCode.J_IF_MOVE_NOT_IN_SET:
            target,move_id,label=args; mon=self.defender if target==Target.DEFENDER else self.attacker
            self._jump(script,label) if all(m.id!=int(move_id) for m in mon.moves) else None
        elif op==OpCode.CALL:
            (label,)=args; self._call(script,label)
        elif op==OpCode.JUMP:
            (label,)=args; self._jump(script,label)
        elif op==OpCode.RETURN_TO_BATTLE:
            if not self.stack: self.running=False
            else: self.pc=self.stack.pop()
        elif op==OpCode.J_IF_LEVELS_ARE:
            value,label=args
            if int(value)==1 and self.attacker.level<self.defender.level: self._jump(script,label)
        else:
            raise NotImplementedError(f"Opcode not implemented: {op}")

    def common_scoring_pass(self):
        mv=self._current_move()
        self.viability[self.considered_move_index]+=max(0, mv.power//10)
        if mv.type in self.attacker.types: self.viability[self.considered_move_index]+=3
        mult=type_effectiveness(mv.type, self.defender.types, self.defender.ability)
        if mult>=2.0: self.viability[self.considered_move_index]+=8
        elif 0<mult<=0.5: self.viability[self.considered_move_index]-=4
        elif mult==0.0: self.viability[self.considered_move_index]-=20
        if would_KO(self.attacker,self.defender,mv,self.battle.weather): self.viability[self.considered_move_index]+=15

MOVE_ID={"DREAM_EATER":0x8A,"EARTHQUAKE":0x59,"THUNDERBOLT":0x55,"TACKLE":0x21,"HYPER_BEAM":0x3F}
CATALOG={
    MOVE_ID["DREAM_EATER"]:Move(MOVE_ID["DREAM_EATER"],"Dream Eater",Type.PSYCHIC,100,100,1),
    MOVE_ID["EARTHQUAKE"]: Move(MOVE_ID["EARTHQUAKE"], "Earthquake", Type.GROUND,100,100,0),
    MOVE_ID["THUNDERBOLT"]:Move(MOVE_ID["THUNDERBOLT"],"Thunderbolt",Type.ELECTRIC,90,100,1),
    MOVE_ID["TACKLE"]:     Move(MOVE_ID["TACKLE"],     "Tackle",     Type.NORMAL, 40,100,0),
    MOVE_ID["HYPER_BEAM"]: Move(MOVE_ID["HYPER_BEAM"], "Hyper Beam", Type.NORMAL,150, 90,1),
}

def build_demo_script()->Script:
    s=Script()
    s.label("START")
    s.emit(OpCode.GET_POWER_OF_STRONGEST)
    s.emit(OpCode.J_IF_BYTE_EQ,0,"FAIL")
    s.emit(OpCode.GET_ABILITY, Target.DEFENDER)
    s.emit(OpCode.J_IF_BYTE_EQ, int(Ability.WONDER_GUARD), "WG_CHECK")
    s.jmp("AFTER_WG")
    s.label("WG_CHECK")
    s.emit(OpCode.J_IF_DMG_BONUS_EQ,0,EFFECT_NEUTRAL,"FAIL")
    s.emit(OpCode.J_IF_DMG_BONUS_EQ,0,EFFECT_RESIST,"FAIL")
    s.emit(OpCode.J_IF_DMG_BONUS_EQ,0,EFFECT_DOUBLE_RESIST,"FAIL")
    s.emit(OpCode.J_IF_DMG_BONUS_EQ,0,EFFECT_IMMUNE,"FAIL")
    s.label("AFTER_WG")
    s.emit(OpCode.GET_ABILITY, Target.DEFENDER)
    s.emit(OpCode.J_IF_BYTE_EQ, int(Ability.DAMP), "DAMP_PATH")
    s.jmp("AFTER_DAMP")
    s.label("DAMP_PATH")
    s.emit(OpCode.GET_TYPE,"MOVE")
    s.emit(OpCode.J_IF_BYTE_EQ, int(Type.GROUND), "FAIL")
    s.label("AFTER_DAMP")
    s.emit(OpCode.J_IF_MOVE_ID_EQ, MOVE_ID["DREAM_EATER"], "DREAM_PATH")
    s.jmp("AFTER_DREAM")
    s.label("DREAM_PATH")
    s.emit(OpCode.J_IF_STATUS1_NEQ, Target.DEFENDER, int(MajorStatus.SLEEP), "FAIL")
    s.label("AFTER_DREAM")
    s.emit(OpCode.GET_ABILITY, Target.DEFENDER)
    s.emit(OpCode.J_IF_BYTE_EQ, int(Ability.STURDY), "STURDY_PATH")
    s.jmp("SCORING")
    s.label("STURDY_PATH")
    s.emit(OpCode.J_IF_DMG_BONUS_EQ,0,EFFECT_IMMUNE,"FAIL")
    s.label("SCORING")
    s.emit(OpCode.ADD_VIABILITY,2)
    s.emit(OpCode.J_IF_MOVE_KO, "BIG_BONUS")
    s.jmp("END_SCORING")
    s.label("BIG_BONUS")
    s.emit(OpCode.ADD_VIABILITY,15)
    s.label("END_SCORING")
    s.ret()
    s.label("FAIL")
    s.emit(OpCode.ADD_VIABILITY,-20)
    s.ret()
    return s

def demo():
    rng=random.Random(0)
    gengar=Pokemon("Gengar",50,(Type.GHOST,Type.POISON),Ability.LEVITATE,150,150,65,60,130,75,110,MajorStatus.NONE,[
        CATALOG[MOVE_ID["DREAM_EATER"]], CATALOG[MOVE_ID["THUNDERBOLT"]], CATALOG[MOVE_ID["TACKLE"]], CATALOG[MOVE_ID["HYPER_BEAM"]]
    ])
    snorlax=Pokemon("Snorlax",50,(Type.NORMAL,None),Ability.WONDER_GUARD,250,250,110,65,65,110,30,MajorStatus.SLEEP,[
        CATALOG[MOVE_ID["TACKLE"]]
    ])
    battle=Battle(Side(gengar), Side(snorlax), Weather.CLEAR)
    script=build_demo_script(); vm=AIVM(battle,rng); choice_idx=vm.run(script)
    return {"chosen_move": gengar.moves[choice_idx].name, "viability_scores": vm.viability, "weather": Weather(battle.weather).name}

if __name__=="__main__":
    import json; print(json.dumps(demo(), indent=2))
