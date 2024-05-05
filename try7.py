import re

def calculate_edit_distance_with_markers(seq1, seq2):
    """
    Calculate the edit distance between two sequences, seq1 and seq2, and annotate transformations.
    """
    m, n = len(seq1), len(seq2)
    dp = [[[0, ''] for _ in range(n + 1)] for _ in range(m + 1)]

    for i in range(1, m + 1):
        dp[i][0] = [i, dp[i-1][0][1] + f"{i}del({seq1[i-1]}) "]
    for j in range(1, n + 1):
        dp[0][j] = [j, dp[0][j-1][1] + f"{j}ins({seq2[j-1]}) "]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i-1] == seq2[j-1]:
                dp[i][j] = [dp[i-1][j-1][0], dp[i-1][j-1][1]]
            else:
                choices = [
                    (dp[i-1][j][0] + 1, dp[i-1][j][1] + f"{i}del({seq1[i-1]}) "),
                    (dp[i][j-1][0] + 1, dp[i][j-1][1] + f"{i}ins({seq2[j-1]}) "),
                    (dp[i-1][j-1][0] + 1, dp[i-1][j-1][1] + f"{i}sub({seq1[i-1]}->{seq2[j-1]}) ")
                ]
                dp[i][j] = min(choices, key=lambda x: x[0])

    return dp[m][n][0], dp[m][n][1].strip()

def find_most_similar_segment(seq1, seq2):
    min_distance = float('inf')
    best_segment = ''
    best_operations = ''
    
    for i in range(len(seq1) - len(seq2) + 1):
        segment = seq1[i:i + len(seq2)]
        distance, operations = calculate_edit_distance_with_markers(segment, seq2)
        if distance < min_distance:
            min_distance = distance
            best_segment = segment
            best_operations = operations
            segment_index = i

    marked_sequence = seq1[:segment_index] + '*' + seq1[segment_index:segment_index + len(seq2)] + '*' + seq1[segment_index + len(seq2):]
    return marked_sequence, min_distance, best_operations

sequence_1 = input("Enter Sequence 1: ").strip().upper()
sequence_2 = input("Enter Sequence 2: ").strip().upper()

marked_sequence, number_of_edits, operations = find_most_similar_segment(sequence_1, sequence_2)

print(f"The marked similar segment in Sequence 1 is: {marked_sequence}")
print(f"Operations to transform into Sequence 2: {operations}")
print(f"The number of edits required is: {number_of_edits}")
