import unittest
import json_parser


class JSReqTest(unittest.TestCase):
    def test_ping_answer(self):
        jstr = '{"req": "PING", "v": 1, "req_id": "0x0666", "arg": {}}\r\n'
        jparser = json_parser.JsonParser(jstr)
        res = jparser.get_result()
        self.assertEqual('{"req_answ": "PING", "err_code": "0x00", "req_id": "0x0666", "v": 1}\r\n', res['txt'])

    def test_ping_is_answer(self):
        jstr = '{"req": "PING", "v": 1, "req_id": "0x0666", "arg": {}}\r\n'
        jparser = json_parser.JsonParser(jstr)
        res = jparser.get_result()
        self.assertTrue(res['has_answer'])

    def test_event(self):
        jstr = '{"req":"EVENT", "req_id":"0x0006","v":1,' \
               '"arg": {"e": [{"dn2": "0x07", "ef":"0x01","ton": [], ' \
               '"toc":"0x06","tm":"0101000018","dn1":"0x00","dt2":"0x0C06","et":"0x0040","dc2":"0x08","dc1":"0x03"}]}}\r\n'
        jparser = json_parser.JsonParser(jstr)
        res = jparser.get_result()
        self.assertEqual('{"req_answ": "EVENT", "err_code": "0x00", "req_id": "0x0006", "v": 1}\r\n', res['txt'])



if __name__ == '__main__':
    unittest.main()
