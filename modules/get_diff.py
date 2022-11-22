#!/usr/bin/env python3
import os
import sys
import base64
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_bytes, to_native

def decode_b64(str):
    str = str.encode('ascii')
    str = base64.b64decode(str)
    str = str.decode('ascii')
    return str

def main():
    module_args = dict(
        f1=dict(required=True, type="str"),
        f2=dict(required=True, type="str"),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)
    err = False

    f1 = decode_b64(module.params['f1'])
    f2 = decode_b64(module.params['f2'])

    print(f1)
    print(f2)

    if err:
        module.fail_json(msg="Error")
    else:
        result = dict(
            changed=True, Response="Success in getting the difference between the files"
        )
        module.exit_json(**result)


if __name__ == "__main__":
    main()
