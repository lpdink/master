import os
import re
import spacy

ZH_FILE=os.path.join(os.path.dirname(__file__), "../resources/corpus/zh_corpus.txt")
EN_FILE=os.path.join(os.path.dirname(__file__), "../resources/corpus/en_corpus.txt")

RESULT_FOLDER=os.path.join(os.path.dirname(__file__), "../resources/preprocess_/")
RESULT_ZH_FILE = os.path.join(RESULT_FOLDER, "zh_corpus_preprocess.txt")
RESULT_EN_FILE = os.path.join(RESULT_FOLDER, "en_corpus_preprocess.txt")

def main():
    illegal_syms = u"�|&|\(|（"
    # 排除zh中含有非法字符的句子
    # 这里，我们认为所有带有(或（注解的句子都非法。
    with open(ZH_FILE, "r") as file:
        zh_lines = file.readlines()
    with open(EN_FILE, "r") as file:
        en_lines = file.readlines()
    assert len(zh_lines)==len(en_lines), f"zh lines {len(zh_lines)} not eq to en lines {len(en_lines)}"
    en_rst, zh_rst = [], []
    for zh_line, en_line in zip(zh_lines, en_lines):
        if re.search(illegal_syms, zh_line) is None:
            zh_rst.append(zh_line)
            en_rst.append(en_line)
    with open(RESULT_ZH_FILE, "w") as file:
        file.writelines(zh_rst)
    with open(RESULT_EN_FILE, "w") as file:
        file.writelines(en_rst)



if __name__ == "__main__":
    main()
