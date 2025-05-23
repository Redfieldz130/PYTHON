# libreria/auth_backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from ldap3 import Server, Connection, NTLM, ALL

class ActiveDirectoryBackend(BaseBackend):
    """
    Autentica contra un AD on-premise usando ldap3.
    """
    def authenticate(self, request, username=None, password=None):
        # Ajusta estos valores a tu entorno
        AD_SERVER   = 'ldap://192.168.0.10'
        AD_DOMAIN   = 'TU_DOMINIO'            # sin sufijo, ej: IDEICE o MIDOMINIO
        SEARCH_DN   = 'OU=Usuarios,DC=tu_dominio,DC=local'

        user_dn = f'{AD_DOMAIN}\\{username}'
        server  = Server(AD_SERVER, get_info=ALL)
        conn    = Connection(server, user=user_dn, password=password, authentication=NTLM, auto_bind=False)

        try:
            if not conn.bind():
                return None
        except Exception:
            return None

        # Si llegamos hasta aquí, la autenticación fue exitosa.
        # Ahora creamos o actualizamos el User local.
        user, created = User.objects.get_or_create(username=username)
        # opcional: cargar atributos del AD (nombre, email...)
        conn.search(
            SEARCH_DN,
            f'(sAMAccountName={username})',
            attributes=['givenName','sn','mail']
        )
        if conn.entries:
            entry = conn.entries[0]
            user.first_name = entry.givenName.value or ''
            user.last_name  = entry.sn.value or ''
            user.email      = entry.mail.value or ''
            user.save()
        conn.unbind()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None