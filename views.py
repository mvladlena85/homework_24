import os
from typing import Any, Optional, Dict

from flask import Blueprint, request, jsonify, Response
from marshmallow import ValidationError

from config import DATA_DIR
from tools import dict_to_list, file_gen, query
from models import RequestSchema

main_bp = Blueprint('main', __name__)


@main_bp.route("/perform_query", methods=['POST'])
def perform_query() -> Any:
    request_data = request.json
    if request_data is None:
        return "пустое тело запроса", 404

    try:
        # валидация данных request_data
        RequestSchema().load(request_data)
        file_path = os.path.join(DATA_DIR, request_data.get("file_name"))

        data = dict_to_list(request_data)
        gen = file_gen(file_path)
        result = None

        for p, v in data:
            if result is None:
                result = query(p, v, gen)
                continue
            result = query(p, v, result)

        if result is None:
            return "Нет данных, отвечающих критериям фильтрации.", 200

        return jsonify(list(result))

    except ValidationError as e:
        return e.messages, 404
    except (TypeError, FileNotFoundError):
        return "некорректно указано имя файла", 404
    except ValueError:
        return "указаны некорректные значения value для команд limit и/или map", 404
