from app.services.linkedin_publisher import publish_linkedin_post

access_token = "PEGA_AQUI_TU_TOKEN"
person_urn = "PEGA_AQUI_TU_URN"

text = "🚀 Prueba directa desde sistema automático."

status, response = publish_linkedin_post(
    access_token=access_token,
    person_urn=person_urn,
    text=text
)

print("STATUS:", status)
print("RESPONSE:", response)