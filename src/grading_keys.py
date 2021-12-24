first = "| Note | Punkte |\n" \
        "|------|--------|\n" \
        "| 1.0  | 86     |\n" \
        "| 1.3  | 82     |\n" \
        "| 1.7  | 78     |\n" \
        "| 2.0  | 74     |\n" \
        "| 2.3  | 70     |\n" \
        "| 2.7  | 66     |\n" \
        "| 3.0  | 62     |\n" \
        "| 3.3  | 58     |\n" \
        "| 3.7  | 54     |\n" \
        "| 4.0  | 50     |\n"

second = "| Note | Punkte |\n" \
        "|------|--------|\n" \
        "| 1.0  | 95     |\n" \
        "| 1.3  | 90     |\n" \
        "| 1.7  | 85     |\n" \
        "| 2.0  | 80     |\n" \
        "| 2.3  | 75     |\n" \
        "| 2.7  | 70     |\n" \
        "| 3.0  | 65     |\n" \
        "| 3.3  | 60     |\n" \
        "| 3.7  | 55     |\n" \
        "| 4.0  | 50     |\n"

third = "| Note | Punkte |\n" \
        "|------|--------|\n" \
        "| 1.0  | 85     |\n" \
        "| 1.3  | 80     |\n" \
        "| 1.7  | 75     |\n" \
        "| 2.0  | 70     |\n" \
        "| 2.3  | 65     |\n" \
        "| 2.7  | 60     |\n" \
        "| 3.0  | 55     |\n" \
        "| 3.3  | 50     |\n" \
        "| 3.7  | 45     |\n" \
        "| 4.0  | 40     |\n"


def which_key(string):
        if string == "86.0":
                return first
        elif string == "95.0":
                return second
        elif string == "40.0":
                return third
        elif string == "0":
                return "Leider gibt es keinen Notenschlüssel für dieses Modul"