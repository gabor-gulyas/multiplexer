import io
import time
##
input_file = "E:/CAGE/fastq/all_read_20230131_CAGE.fastq"
output_folder = "E:/CAGE/output_3nd_seq_test/1st/"
sequences = ["ACCG", "CACG", "AGTG", "GCGG", "ATGG", "TACG", "ACGG", "GCTG"]

start_time = time.time()
files = {}
buffers = {}
for sequence in sequences:
    buffer = io.StringIO()
    files[sequence] = open(f"{output_folder}/{sequence}.fastq", "w")
    buffers[sequence] = buffer

with open(input_file, "r") as f:
    reads = []
    lines = []
    for line in f:
        lines.append(line.strip())
        if len(lines) == 4:
            read = lines
            sequence = lines[1][:4]
            if sequence in sequences:
                buffer = buffers[sequence]
                buffer.write("\n".join(read) + "\n")
                if buffer.tell() > 100000:  # Flush buffer if it reaches a certain size
                    files[sequence].write(buffer.getvalue())
                    buffer.seek(0)
                    buffer.truncate(0)
            lines = []

for sequence in sequences:
    buffer = buffers[sequence]
    files[sequence].write(buffer.getvalue())
    buffer.close()
    files[sequence].close()

end_time = time.time()
print("Execution time: {:.2f} seconds".format(end_time - start_time))