#!/usr/bin/env bash
# Teste l'API QuickBite sécurisée par Keycloak, en obtenant de vrais tokens.
# S'exécute DANS le réseau docker (pour que l'issuer http://keycloak:8080 corresponde).
# Usage : ./test-api.sh
set -e
NET="$(docker compose ps -q >/dev/null 2>&1 && basename "$PWD")_qb-net"
NET="${NET:-quickbite-keycloak_qb-net}"

cq() { docker run --rm --network "$NET" curlimages/curl:8.10.1 "$@" 2>/dev/null; }

tok() {
  cq -s -X POST http://keycloak:8080/realms/quickbite/protocol/openid-connect/token \
     -d "client_id=quickbite" -d "grant_type=password" \
     -d "username=$1" -d "password=$2" \
  | python3 -c "import sys,json;print(json.load(sys.stdin).get('access_token',''))"
}

api() { cq -s "$@" http://api:8080"$1"; }   # raccourci non utilisé (gardé pour clarté)
code() { cq -s -o /dev/null -w "%{http_code}" "$@"; }

pass=0; fail=0
check() { # libellé  attendu  code
  if [ "$2" = "$3" ]; then echo "  ✅ $1 -> $3"; pass=$((pass+1));
  else echo "  ❌ $1 -> $3 (attendu $2)"; fail=$((fail+1)); fi
}

echo "Façade /auth (signup, login, refresh) :"
U="user$RANDOM"
check "POST /auth/register" 201 "$(code -X POST http://api:8080/auth/register -H 'Content-Type: application/json' -d "{\"username\":\"$U\",\"email\":\"$U@quickbite.local\",\"password\":\"secret123\"}")"
NEW=$(cq -s -X POST http://api:8080/auth/login -H 'Content-Type: application/json' -d "{\"username\":\"$U\",\"password\":\"secret123\"}")
NREF=$(echo "$NEW" | python3 -c "import sys,json;print(json.load(sys.stdin).get('refresh_token',''))")
[ -n "$NREF" ] && { echo "  ✅ POST /auth/login (compte créé) -> token OK"; pass=$((pass+1)); } || { echo "  ❌ login du compte créé"; fail=$((fail+1)); }
check "POST /auth/refresh" 200 "$(code -X POST http://api:8080/auth/refresh -H 'Content-Type: application/json' -d "{\"refreshToken\":\"$NREF\"}")"

echo "Obtention des tokens (via la façade /auth/login) …"
login() { cq -s -X POST http://api:8080/auth/login -H 'Content-Type: application/json' -d "{\"username\":\"$1\",\"password\":\"$2\"}" | python3 -c "import sys,json;print(json.load(sys.stdin).get('access_token',''))"; }
AT=$(login admin admin)
CT=$(login client client)
[ -z "$AT" ] && { echo "Échec : pas de token admin (Keycloak prêt ?)"; exit 1; }

echo "Tests RBAC :"
check "/health (public)"        200 "$(code http://api:8080/health)"
check "/me sans token"          401 "$(code http://api:8080/me)"
check "/me (admin)"             200 "$(code -H "Authorization: Bearer $AT" http://api:8080/me)"
check "/orders (client)"        200 "$(code -H "Authorization: Bearer $CT" http://api:8080/orders)"
check "/admin/summary (admin)"  200 "$(code -H "Authorization: Bearer $AT" http://api:8080/admin/summary)"
check "/admin/summary (client)" 403 "$(code -H "Authorization: Bearer $CT" http://api:8080/admin/summary)"

echo "Résultat : $pass réussis, $fail échoués"
exit $fail
