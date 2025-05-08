# scripts/data_validation/validation_schemas.py

# ─── Train Schema (기존 그대로) ─────────────────────────────
train_schema = {
    "type": "object",
    "required": [
        "mass_full_bin", "mass_empty_bin", "num_full_bins", "num_empty_bins",
        "mass_locomotive", "mass_brakevan", "has_brakevan",
        "rolling_resistance_full", "rolling_resistance_empty",
        "rolling_resistance_locomotive_drive", "rolling_resistance_brakevan",
        "curve_resistance_factor",
        "tractive_effort_curve"
    ],
    "properties": {
        "mass_full_bin": {"type": "number"},
        "mass_empty_bin": {"type": "number"},
        "num_full_bins": {"type": "integer"},
        "num_empty_bins": {"type": "integer"},
        "mass_locomotive": {"type": "number"},
        "mass_brakevan": {"type": "number"},
        "has_brakevan": {"type": "integer", "enum": [0, 1]},

        "rolling_resistance_full": {"type": "number"},
        "rolling_resistance_empty": {"type": "number"},
        "rolling_resistance_locomotive_drive": {"type": "number"},
        "rolling_resistance_brakevan": {"type": "number"},

        "curve_resistance_factor": {"type": "number"},

        "tractive_effort_curve": {
            "type": "object",
            "patternProperties": {
                "^\\d+$": {"type": "number"}
            }
        }
    },
    "additionalProperties": False
}


# ─── New: Track Segment Schema (하나의 세그먼트 기준) ─────────────
track_segment_schema = {
    "type": "object",
    "required": [
        "Radius", "CurveID", "X_Center", "Y_Center",
        "Min_Slope", "Max_Slope", "Avg_Slope",
        "Length", "Z_Min", "Z_Max", "Z_Mean",
        "XStart", "YStart", "XFinish", "YFinish"
    ],
        "properties": {
        "Radius": {"type": ["number", "null"]},
        "CurveID": {"type": ["number", "null"]},
        "X_Center": {"type": ["number", "null"]},
        "Y_Center": {"type": ["number", "null"]},
        "Min_Slope": {"type": ["number", "null"]},
        "Max_Slope": {"type": ["number", "null"]},
        "Avg_Slope": {"type": ["number", "null"]},
        "Length": {"type": ["number", "null"]},
        "Z_Min": {"type": ["number", "null"]},
        "Z_Max": {"type": ["number", "null"]},
        "Z_Mean": {"type": ["number", "null"]},
        "XStart": {"type": ["number", "null"]},
        "YStart": {"type": ["number", "null"]},
        "XFinish": {"type": ["number", "null"]},
        "YFinish": {"type": ["number", "null"]}
    },

    "additionalProperties": True
}
