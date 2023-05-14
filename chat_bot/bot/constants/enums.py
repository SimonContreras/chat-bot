"""Enums for Discord Bot"""
from enum import Enum


class DefaultMessages(Enum):
    "Default Message for Discord Bot"
    NO_PROFILING_SET = "Hola {author_name} !, creo que es primera vez que hablamos por este chat!, Quieres que tome algun perfil en especifico?, reacciona con  ✅  para darme un perfil, sino, reacciona  ❌  para continuar conversando ..."
    REACT_TO_MESSAGE_OTHERWISE_BLOCK = "Por favor reacciona a este mensaje con  ✅  o con  ❌ para poder continuar con nuestra conversacion."


class Prefix(Enum):
    "Prefixes for bot"
    QUESTION_MARK = "?"
