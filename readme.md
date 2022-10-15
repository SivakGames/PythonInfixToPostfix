# Python Infix to Postfix Converter

Simple program meant to take an infix mathematical expression as a string, tokenize it (discarding excess whitespace), then convert it into postfix tokens and ultimately calculate the end result if possible.

The process of converting utilizes the Shunting Yard algorithm.

I'm sure there could be some slight optimizations in the code, but overall it works as intended.

## How to use

Simply pass a string to the `infixExpressionToPostfix` that is a mathematical expression.

Right now, there are just a few simple examples provided at the end of the main function.

If the expression is invalid, errors explaining why will be logged.  If it is valid, then the result will be printed out.

## Valid operators

- Numbers (can be binary or hexadecimal as well)
  - Currently cannot take anything with decimal points, but it can convert those
- The binary operators for arithmetic: `+ - * / %`
  - For unary negative signs: Simply input a `-` where desired (will be converted to the negation token of `¬` upon detection. Do NOT enter `¬`)
- The binary bitwise operators: `^ & | << >>`
- The unary bitwise operator: `~`
- Parentheses: `( )`
- Single argument functions (right now only `sin`, `cos`, `sqrt`)
- User-defined variables

## Credits

Developed by: Sivak Games

## References

These sites offered the most help with explaining how parts of the algorithm work.

- <https://www.andr.mu/logs/the-shunting-yard-algorithm/>

- <https://exchangetuts.com/infix-to-postfix-for-negative-numbers-1641157504843695>



