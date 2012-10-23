if __name__=='__main__':
    import os, sys, re
    
import ldap, sys
ldap.set_option(ldap.OPT_REFERRALS, 0)
ldap.set_option(ldap.OPT_PROTOCOL_VERSION, ldap.VERSION3)
#allow a self-signed cert, for now
ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)

LDAP_SERVER = 'ldap://10.242.28.54'
AD_BIND_DN = 'accounttest@rcdev.domain'
AD_BIND_PW = '!3ZW&5!X'
BASE_DOMAIN = 'ou=Domain Users,dc=rcdev,dc=domain'
NEW_ACCOUNT_OU = 'ou=new_accounts'

class LdapConnection:
    #connect to the server
    def __init__(self, ldap_server=None):
        self.conn = ldap.initialize(ldap_server)
        self.conn.simple_bind_s(AD_BIND_DN, AD_BIND_PW)

    def unbind(self):
        if not self.conn:
            return
        self.conn.unbind_s()

    def search(self, filter):
        try:
            results = self.conn.search_ext_s(BASE_DOMAIN, ldap.SCOPE_SUBTREE, filter, ['*'])
            return results
        except ldap.NO_SUCH_OBJECT:
            return ldap.NO_SUCH_OBJECT

    def search_by_email(self, email):
        filter = '(&(objectClass=person)(mail=%s))' % (email)
        return self.search(filter)

    def search_by_firstname_lastname(self, firstname, lastname):
        filter = '(&(objectClass=person)(givenName=%s)(sn=%s))' % (firstname,lastname)
        return self.search(filter)

    def search_by_upn(self, uPN):
        filter = '(&(objectClass=person)(userPrincipalName=%s))' % (uPN)
        return self.search(filter)

def test_connection():
    ldap_conn = LdapConnection(LDAP_SERVER)
    print ldap_conn
    ldap_conn.unbind()

def test_search():
    ldap_conn = LdapConnection(LDAP_SERVER)
    results = ldap_conn.search_by_email('lsilva@harvard.edu')
    print results
    results = ldap_conn.search_by_firstname_lastname('Luis', 'Silva')
    print results
    results = ldap_conn.search_by_upn('lsilva@rcdev.domain')
    print results
    ldap_conn.unbind()

if __name__=='__main__':
    test_search()
