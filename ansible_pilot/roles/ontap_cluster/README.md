Role Name
=========

A brief description of the role goes here.

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------

This role currently supports two types of variable inputs:
1) Reading information from the hostvars by specifying the SVM to look for with "ontap_svm_name"
2) passing an object "__ontap_svm_input__"

Optional:
If you want to create a management interface to e.g. configure DNS and CIFS, you can provide a name for that as well with "ontap_ip_interface_name". The name will be either looked up from the hostvars or the input object.

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
