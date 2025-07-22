from hashlib import new as hashlib_new
from Crypto.Hash import MD4
import hashlib
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from ldap3 import Server, Connection, NTLM, ALL
import logging
def md4(data=b''):
    h = MD4.new()
    h.update(data)
    return h

hashlib.new = lambda name, data=b'': md4(data) if name.lower() == 'md4' else hashlib_new(name, data)

logger = logging.getLogger(__name__)

class ActiveDirectoryBackend(BaseBackend):
    AD_SERVER = 'ldap://10.80.10.40'
    AD_DOMAIN = 'ideice'
    SEARCH_DN = 'DC=ideice,DC=local'

    def authenticate(self, request, username=None, password=None):
        logger.info(f"Intentando autenticar usuario: {username}")

        if username is None or password is None:
            return None

        user_dn = f'{self.AD_DOMAIN}\\{username}'
        server = Server(self.AD_SERVER, get_info=ALL)
        conn = Connection(server, user=user_dn, password=password, authentication=NTLM, auto_bind=False)

        try:
            if not conn.bind():
                logger.warning(f"Fallo bind LDAP para usuario {username}: {conn.result}")
                return None
        except Exception as e:
            logger.error(f"Excepción durante bind LDAP para {username}: {e}")
            return None

        user, created = User.objects.get_or_create(username=username)

        conn.search(
            self.SEARCH_DN,
            f'(sAMAccountName={username})',
            attributes=['givenName', 'sn', 'mail']
        )

        if conn.entries:
            entry = conn.entries[0]
            user.first_name = entry.givenName.value or ''
            user.last_name = entry.sn.value or ''
            user.email = entry.mail.value or ''
            user.save()

        conn.unbind()
        logger.info(f"Usuario {username} autenticado correctamente")
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

