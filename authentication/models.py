from django.db import models
import simpleldap

# Create your models here.


class LDAPWrapper(models.Model):

# Constants
    CONNECTION_DOMAIN = 'ldap.uniandes.edu.co'
    BASE_DN = 'ou=People, dc=uniandes, dc=edu, dc=co'

# Attributes
    conn = None

    @classmethod
    def create(cls):
        me = cls()
        me.conn = simpleldap.Connection(LDAPWrapper.CONNECTION_DOMAIN)
        me.conn = simpleldap.Connection('ldap.uniandes.edu.co')
        return me


    def authenticate(self, login, password):
        """
        :type login str
        :type password str
        """
        user = login.strip().lower() or "Ninguno"
        password = password or "Ninguno"

        self.conn = simpleldap.Connection(LDAPWrapper.CONNECTION_DOMAIN)
        is_valid = self.conn.authenticate('uid='+user+', ' + self.BASE_DN, password)

        return is_valid

    def search(self, user):
        data = self.conn.get('uid='+ user, base_dn=self.BASE_DN)
        return data