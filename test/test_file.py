from pybite.file import *


test_data = [
    "Name;Age;",
    "Test;00;",
    "Test;11;",
    "John;22;",
    "Test;33;",
    "Test;44;",
    "Test;55;",
    "Test;66;",
    "Test;77;",
    "Test;88;",
]


def test_split_by_lines(tmpdir):
    input_path = tmpdir.join("test.txt").strpath
    output_path = tmpdir.mkdir("out").join("").strpath
    
    with open(input_path, "w") as f:
        f.write("\n".join(test_data))

    chunk_files = split_by_lines(input_path, output_path, 4, 
    persist_header=True)

    assert len(chunk_files) == 3

    header, data = test_data[0], test_data[1:]
    for i in range(0, 3):
        file_name = chunk_files[i]
        _chunk_data = [
            header,
            *data[i * 4:(i+ 1) * 4]
        ]
        with open(file_name, "r") as f:
            assert f.read() == "\n".join(_chunk_data) + "\n"
    pass