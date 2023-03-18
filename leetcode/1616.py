# https://leetcode.cn/problems/split-two-strings-to-make-palindrome/
"""给你两个字符串 a 和 b ，它们长度相同。请你选择一个下标，将两个字符串都在 相同的下标 分割开。由 a 可以得到两个字符串： aprefix 和 asuffix ，满足 a = aprefix + asuffix ，同理，由 b 可以得到两个字符串 bprefix 和 bsuffix ，满足 b = bprefix + bsuffix 。请你判断 aprefix + bsuffix 或者 bprefix + asuffix 能否构成回文串。

当你将一个字符串 s 分割成 sprefix 和 ssuffix 时， ssuffix 或者 sprefix 可以为空。比方说， s = "abc" 那么 "" + "abc" ， "a" + "bc" ， "ab" + "c" 和 "abc" + "" 都是合法分割。

如果 能构成回文字符串 ，那么请返回 true，否则返回 false 。

注意， x + y 表示连接字符串 x 和 y 。

 

示例 1：

输入：a = "x", b = "y"
输出：true
解释：如果 a 或者 b 是回文串，那么答案一定为 true ，因为你可以如下分割：
aprefix = "", asuffix = "x"
bprefix = "", bsuffix = "y"
那么 aprefix + bsuffix = "" + "y" = "y" 是回文串。
示例 2：

输入：a = "abdef", b = "fecab"
输出：true
示例 3：

输入：a = "ulacfd", b = "jizalu"
输出：true
解释：在下标为 3 处分割：
aprefix = "ula", asuffix = "cfd"
bprefix = "jiz", bsuffix = "alu"
那么 aprefix + bsuffix = "ula" + "alu" = "ulaalu" 是回文串。
 

提示：

1 <= a.length, b.length <= 105
a.length == b.length
a 和 b 都只包含小写英文字母
"""
#######################################################################################
"""解题：
首先写出本题目的暴力破解版，以为是双循环，执行了一次发现有问题。才发现题目要求a和b字符串的切割索引相同，是个单循环。
改成单循环版本，考察时间瓶颈，注意到字符串的回文比较本身比较慢，包裹在循环里不断进行不恰当。
故必然存在规律。考虑返回True的情况。注意到题目的实质，实际上是选择一个index，用b[index:]替换a[index:]，使得a是个回文，交换a,b亦然。
故可以直接判断a[:index]和b[index:]是否是回文。交换a,b依然。

## 第一次提交：
# 忘记考虑交换a,b的情况了。审查条件写成：if a[i]!=b[-i-1]，错误。更改审查条件为：a[i]!=b[-i-1] and a[-i-1]!=b[i]

## 第二次提交：
# 忘记考虑case "pvhmupgqeltozftlmfjjde" "yjgpzbezspnnpszebzmhvp"
这一case实际上是：
"pvhm upgqeltozftlmfjjde" "yjgp zbezspnnpszebz mhvp"
这是一种未被考虑到的情况，即if a[i]!=b[-i-1] and a[-i-1]!=b[i]时，有可能剩余的a或b的中间串自身回文。
因此，将判断体内语句从return False更改为return (ishuiwen(a[i:-i]) or ishuiwen(b[i:-i])) and i>0

PASS
"""


def ishuiwen(s):
    return s == s[::-1]


class Solution:
    def checkPalindromeFormation(self, a: str, b: str) -> bool:
        for i in range(int(len(a) / 2)):
            if a[i] != b[-i - 1] and a[-i - 1] != b[i]:
                return (ishuiwen(a[i:-i]) or ishuiwen(b[i:-i])) and i > 0
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


if __name__ == "__main__":
    s = Solution()
    s.checkPalindromeFormation("xbdef", "xecab")
