"""Interpret record boundaries while preserving the submitted text exactly."""

from io import StringIO

from molsysmt._private.smonitor import FormatError


def parse_source_records(text, source):
    records = []
    header = None
    sequence = []
    start = offset = 0
    preamble = text

    def finish(stop):
        records.append(
            {
                "record_index": len(records),
                "header": header,
                "sequence": "".join(sequence),
                "raw_record": text[start:stop],
                "source_span": [start, stop],
            }
        )

    # Universal newline recognition without translating CR, LF or CRLF bytes
    # in the decoded text. Other Unicode separators remain sequence content.
    for number, line in enumerate(StringIO(text, newline=""), start=1):
        content = line.removesuffix("\n").removesuffix("\r")
        if content.startswith(">"):
            if header is None:
                preamble = text[:offset]
            else:
                finish(offset)
            header, sequence, start = content[1:], [], offset
        elif header is None:
            if content.strip():
                raise FormatError(
                    reason=f"FASTA content before the first header at line {number}."
                )
        else:
            sequence.append(content)
        offset += len(line)
    if header is not None:
        finish(len(text))

    return {
        "schema": "molsysmt.fasta_source@1",
        "source": source,
        "preamble": preamble,
        "records": records,
    }
