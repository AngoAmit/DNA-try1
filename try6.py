import re

def calculate_edit_distance_with_markers(seq1, seq2):
    """
    Calculate the edit distance between two sequences seq1 and seq2 with detailed editing operations.
    """
    m, n = len(seq1), len(seq2)
    dp = [[[0, '']] * (n + 1) for _ in range(m + 1)]

    # Initialize the base cases
    for i in range(1, m + 1):
        dp[i][0] = [i, dp[i-1][0][1] + f"del({seq1[i-1]} {i}) "]
    for j in range(1, n + 1):
        dp[0][j] = [j, dp[0][j-1][1] + f"ins({seq2[j-1]} 0) "]

    # Calculate edit distances and operations
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i-1] == seq2[j-1]:
                dp[i][j] = [dp[i-1][j-1][0], dp[i-1][j-1][1]]
            else:
                choices = [
                    (dp[i-1][j][0] + 1, dp[i-1][j][1] + f"del({seq1[i-1]} {i}) "),
                    (dp[i][j-1][0] + 1, dp[i][j-1][1] + f"ins({seq2[j-1]} {i}) "),
                    (dp[i-1][j-1][0] + 1, dp[i-1][j-1][1] + f"sub({seq1[i-1]}->{seq2[j-1]} {i}) ")
                ]
                dp[i][j] = min(choices, key=lambda x: x[0])

    # Retrieve the operations and count of deletions
    edits = dp[m][n][1].strip().split('\n')
    num_deletions = sum(1 for edit in edits if edit.startswith('del'))

    return dp[m][n][0], dp[m][n][1], num_deletions

def find_most_similar_segment(seq1, seq2):
    """
    Find the segments in seq1 that are most similar to seq2 and calculate the detailed edit distance.
    """
    min_distance = float('inf')
    best_operations = ""
    segment_index = 0
    num_deletions = 0

    # Searching for the best match segment in seq1
    for i in range(len(seq1) - len(seq2) + 1):
        segment = seq1[i:i+len(seq2)]
        if re.match("^[ATGC]*$", segment):  # Validate the segment
            distance, operations, deletions = calculate_edit_distance_with_markers(segment, seq2)
            if distance < min_distance:
                min_distance = distance
                best_operations = operations
                segment_index = i
                num_deletions = deletions

    marked_sequence = seq1[:segment_index] + '*' + seq1[segment_index:segment_index + len(seq2)] + '*' + seq1[segment_index + len(seq2):]
    return marked_sequence, min_distance, best_operations, num_deletions

# User input and outputs handling
sequence_1 = input("Enter Sequence 1: ").strip().upper()
sequence_2 = input("Enter Sequence 2: ").strip().upper()

marked_sequence, number_of_edits, operations, num_deletions = find_most_similar_segment(sequence_1, sequence_2)

print(f"The marked similar segment in Sequence 1 is: {marked_sequence}")
print(f"Operations to transform into Sequence 2: {operations}")
print(f"The number of edits required is: {number_of_edits}")
print(f"Minimum number of deletions is: {num_deletions}")
