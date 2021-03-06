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


def test_iterate_file_by_lines(tmpdir):
    input_path = tmpdir.join("test.txt").strpath

    with open(input_path, "w") as f:
        f.write("\n".join(test_data))

    lines = iterate_file_by_lines(input_path, strip_end=True)
    assert "\n".join(test_data) == "\n".join(lines)


def test_split_file_by_lines(tmpdir):
    input_path = tmpdir.join("test.txt").strpath
    output_path = tmpdir.mkdir("out").join("").strpath

    with open(input_path, "w") as f:
        f.write("\n".join(test_data))

    chunk_files = split_file_by_lines(input_path, output_path, 4,
                                      persist_header=True)

    assert len(chunk_files) == 3

    header, data = test_data[0], test_data[1:]
    for i in range(0, 3):
        file_name = chunk_files[i]
        _chunk_data = [
            header,
            *data[i * 4:(i + 1) * 4]
        ]
        with open(file_name, "r") as f:
            assert f.read().strip() == "\n".join(_chunk_data)
    pass


def test_join_file_chunks(tmpdir):
    header, data = test_data[0], test_data[1:]
    for i in range(0, 3):
        f = tmpdir.join(f"test.chunk{i:04d}.txt")
        _chunk_data = "\n".join([
            header,
            *data[i * 4:(i + 1) * 4]
        ])
        f.write(_chunk_data)
    actual_data = "\n".join(test_data)
    lines_iter = join_file_chunks(tmpdir.strpath, persisted_header=True)
    joined_lines = "".join(lines_iter)
    assert actual_data == joined_lines


def test_slice_file_by_lines(tmpdir):
    input_path = tmpdir.join("test.txt").strpath

    with open(input_path, "w") as f:
        f.write("\n".join(test_data))
    _slice = slice_file_by_lines(input_path, 0, 6, persist_header=True)
    assert "".join(_slice) == "\n".join(test_data[0:7]) + "\n"

    _slice = slice_file_by_lines(input_path, 3, 1)
    assert "" == "\n".join(_slice)

    _slice = slice_file_by_lines(input_path, 3, 1, persist_header=True)
    assert "".join(_slice) == "\n".join(test_data[:1]) + "\n"
