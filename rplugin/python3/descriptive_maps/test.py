from parser import ParsedLine


test_1 = 'n  ,cc           <Plug>(InYoFace_Toggle)<CR>'
test_2 = 'n  ,cc         *  <Plug>(InYoFace_Toggle)<CR>'

res_1 = ParsedLine(test_1)

assert res_1.mode == "n"
assert res_1.lhs == ",cc"
assert res_1.rhs == "<Plug>(InYoFace_Toggle)<CR>"
assert res_1.source_file == ''
assert res_1.comments == []

res_2 = ParsedLine(test_2)

assert res_2.mode == "n"
assert res_2.lhs == ",cc"
assert res_2.rhs == "<Plug>(InYoFace_Toggle)<CR>"
