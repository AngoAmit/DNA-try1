import re

def calculate_edit_distance(seq1, seq2):
    """
    Calculate the edit distance between two sequences seq1 and seq2.
    """
    # Create a matrix to store the distances
    distances = [[0 for _ in range(len(seq2) + 1)] for _ in range(len(seq1) + 1)]
    
    # Initialize the base case values
    for i in range(len(seq1) + 1):
        distances[i][0] = i
    for j in range(len(seq2) + 1):
        distances[0][j] = j
    
    # Calculate the edit distance matrix using dynamic programming
    for i in range(1, len(seq1) + 1):
        for j in range(1, len(seq2) + 1):
            if seq1[i - 1] == seq2[j - 1]:
                cost = 0
            else:
                cost = 1
            distances[i][j] = min(distances[i - 1][j] + 1,      # Deletion
                                  distances[i][j - 1] + 1,      # Insertion
                                  distances[i - 1][j - 1] + cost)  # Substitution
    return distances[-1][-1]

def find_most_similar_segment(seq1, seq2):
    """
    Find the segments in seq1 that are most similar to seq2 and calculate the edit distance.
    """
    min_distance = float('inf')
    similar_segments = []
    # Search for the best match in the middle of seq1
    for i in range(len(seq1) - len(seq2) + 1):
        segment = seq1[i:i+len(seq2)]
        if re.match("^[ATGC]*$", segment):  # Validate the segment
            distance = calculate_edit_distance(segment, seq2)
            if distance < min_distance:
                min_distance = distance
                similar_segments = [segment]
            elif distance == min_distance:
                similar_segments.append(segment)

    # The most similar segments and their edit distance
    return similar_segments, min_distance

# Take input and validate
while True:
    sequence_1 = input("Enter Sequence 1: ").strip().upper()
    if re.match("^[ATGC]*$", sequence_1):
        break
    else:
        print("Invalid input. The sequence should only contain the letters A, T, G, and C.")

while True:
    sequence_2 = input("Enter Sequence 2: ").strip().upper()
    if re.match("^[ATGC]*$", sequence_2):
        break
    else:
        print("Invalid input. The sequence should only contain the letters A, T, G, and C.")

# Find the most similar segment(s) and the required number of edits
similar_segments, number_of_edits = find_most_similar_segment(sequence_1, sequence_2)

print(f"The most similar segment(s) in Sequence 1 is: {', '.join(similar_segments)}")
print(f"The number of edits required to transform these segment(s) into Sequence 2 is: {number_of_edits}")
