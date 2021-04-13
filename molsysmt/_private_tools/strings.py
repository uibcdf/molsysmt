
def pattern_in_between_patterns(string, in_between, pattern_left, pattern_right):

    output = False

    if (pattern_left in string) and (pattern_right in string) and (in_between in string):
        segments_left = string.split(pattern_left)
        for segment in segments_left[1:]:
            candidate = segment.split(pattern_right)[0]
            if in_between in candidate:
                output = candidate
                break

    return output



