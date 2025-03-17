sudo_str = \
    "53-" "-7-" "---" \
    "6--" "195" "---" \
    "-98" "---" "-6-" \
    "8--" "-6-" "--3" \
    "4--" "8-3" "--1" \
    "7--" "-2-" "--6" \
    "-6-" "---" "28-" \
    "---" "419" "--5" \
    "---" "-8-" "-79"


def chunks_of_9(s: str):
    chunk_size = 9
    return (s[i:chunk_size + i] for i in range(0, len(s), chunk_size))


if __name__ == "__main__":
    print(list(chunks_of_9(sudo_str)))
