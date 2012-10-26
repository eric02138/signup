import ldap, sys
from ldap import modlist
ldap.set_option(ldap.OPT_REFERRALS, 0)
ldap.set_option(ldap.OPT_PROTOCOL_VERSION, ldap.VERSION3)
#allow a self-signed cert, for now
ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)

LDAP_SERVER = 'ldaps://10.242.28.54:636'
AD_BIND_DN = 'accounttest@rcdev.domain'
AD_BIND_PW = '!3ZW&5!X'
DOMAIN_STRING = 'rcdev.domain'
BASE_DOMAIN = 'ou=Domain Users,dc=rcdev,dc=domain'
NEW_ACCOUNT_OU = 'ou=new_accounts,ou=Domain Users,dc=rcdev,dc=domain'

class LdapConnection:
    #connect to the server
    def __init__(self, ldap_server=LDAP_SERVER):
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

    def add_user(self):
        # The dn of our new entry/object

        dn='cn=John Brunelle,%s' % NEW_ACCOUNT_OU

        record_attrs = [
            ('objectclass', ['top', 'person', 'organizationalperson', 'user']),
            ('userPrincipalName', ['jab@%s' % DOMAIN_STRING]),
            ('distinguishedName', [dn]),
            ('sAMAccountName', ['jab']),
            ('mail', ['jab@harvard.edu']),
            ('givenname', ['John']),
            ('sn', ['Brunelle']),
            ('ou', ['new_accounts', 'Domain Users']),
            ('userAccountControl', ['514']),
            ('pwdLastSet', ['-1']),
            ]


        try:
            self.conn.add_s(dn, record_attrs)
        except ldap.LDAPError, error_message:
            print "Error adding new user: %s" % error_message
            return False

        """
        try:
            self.passwd_s(dn, '', 'N0ss1sB0ss!')
        except ldap.LDAPError, error_message:
            print "Goddammit! %s" % error_message
            return False
        """

        return self

    def enable_new_user(self, cn):
        #doesn't work with current AD configuration
        mod_acct = [(ldap.MOD_REPLACE, 'userAccountControl', '512')]
        dn = 'cn=%s,%s' % (cn, NEW_ACCOUNT_OU)
        print dn
        try:
            self.conn.modify_s(dn, mod_acct)
        except ldap.LDAPError, error_message:
            print "Error enabling user: %s" % error_message
            return False
        return True

def test_connection():
    ldap_conn = LdapConnection()
    print ldap_conn
    ldap_conn.unbind()

def test_search():
    ldap_conn = LdapConnection()
    results = ldap_conn.search_by_email('lsilva@harvard.edu')
    print results
    results = ldap_conn.search_by_firstname_lastname('Luis', 'Silva')
    print results
    results = ldap_conn.search_by_upn('lsilva@rcdev.domain')
    print results
    ldap_conn.unbind()

def test_add():
    ldap_conn = LdapConnection()
    print ldap_conn.add_user()
    ldap_conn.unbind()

if __name__=='__main__':
    ldap_conn = LdapConnection()
    #ldap_conn.enable_new_user('John Brunelle')
    ldap_conn.add_user()
    ldap_conn.unbind()
