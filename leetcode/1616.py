# https://leetcode.cn/problems/split-two-strings-to-make-palindrome/
def ishuiwen(s):
    return s==s[::-1]

class Solution:
    def checkPalindromeFormation(self, a: str, b: str) -> bool:
        if len(a)<2:
            return True
        for i in range(int(len(a)/2)):
            if a[i]!=b[-i-1] and a[-i-1]!=b[i]:
                return (ishuiwen(a[i:-i]) or ishuiwen(b[i:-i])) and i>0
        return True

# def ishuiwen(s):
#     return s==s[::-1]

# class Solution:
#     def checkPalindromeFormation(self, a: str, b: str) -> bool:
#         if ishuiwen(a) or ishuiwen(b):
#             return True
#         assert len(a)==len(b)
#         for i in range(len(a)):
#             a_pre, a_suf = a[:i], a[i:]
#             b_pre, b_suf = b[:i], b[i:]
#             if ishuiwen(a_pre+b_suf) or ishuiwen(b_pre+a_suf):
#                 return True
#         return False


if __name__=="__main__":
    s=Solution()
    s.checkPalindromeFormation("xbdef", "xecab")