import json
import re
from abc import ABC, abstractmethod
from typing import Dict, NamedTuple
import pandas as pd
from pilot.utils import build_logger
from pilot.out_parser.base import BaseOutputParser, T
from pilot.configs.model_config import LOGDIR


logger = build_logger("webserver", LOGDIR + "DbChatOutputParser.log")


class PluginAction(NamedTuple):
    command: Dict
    speak: str
    thoughts: str


class PluginChatOutputParser(BaseOutputParser):
    def parse_prompt_response(self, model_out_text) -> T:
        clean_json_str = super().parse_prompt_response(model_out_text)
        print(clean_json_str)
        if not clean_json_str:
            raise ValueError("model server response not have json!")
        try:
            response = json.loads(clean_json_str)
        except Exception as e:
            raise ValueError("model server out not fllow the prompt!")

        command, thoughts, speak = (
            response["command"],
            response["thoughts"],
            response["speak"],
        )
        return PluginAction(command, speak, thoughts)

    def parse_view_response(self, speak, data) -> str:
        ### tool out data to table view
        print(f"parse_view_response:{speak},{str(data)}")
        view_text = f"##### {speak}" + "\n" + str(data)
        return view_text

    def get_format_instructions(self) -> str:
        pass
