import requests
import json


def publish_linkedin_post(access_token: str, person_urn: str, text: str):

    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        "Authorization": f"Bearer {access_token.strip()}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "LinkedIn-Version": "202401"
    }

    payload = {
        "author": f"urn:li:person:{person_urn}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    return response.status_code, response.text


def publish_linkedin_image_post(access_token: str, person_urn: str, text: str, image_path: str):

    headers = {
        "Authorization": f"Bearer {access_token.strip()}",
        "X-Restli-Protocol-Version": "2.0.0",
        "LinkedIn-Version": "202401",
        "Content-Type": "application/json"
    }

    # -----------------------------------
    # STEP 1: REGISTER UPLOAD
    # -----------------------------------
    register_url = "https://api.linkedin.com/v2/assets?action=registerUpload"

    register_payload = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "owner": f"urn:li:person:{person_urn}",
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }
            ]
        }
    }

    register_response = requests.post(
        register_url,
        headers=headers,
        json=register_payload
    )

    if register_response.status_code != 200:
        return register_response.status_code, register_response.text

    register_data = register_response.json()

    upload_url = register_data["value"]["uploadMechanism"][
        "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
    ]["uploadUrl"]

    asset = register_data["value"]["asset"]

    # -----------------------------------
    # STEP 2: UPLOAD BINARY IMAGE
    # -----------------------------------
    with open(image_path, "rb") as img_file:
        upload_response = requests.put(
            upload_url,
            data=img_file,
            headers={
                "Authorization": f"Bearer {access_token.strip()}",
                "LinkedIn-Version": "202401"
            }
        )

    if upload_response.status_code not in [200, 201]:
        return upload_response.status_code, upload_response.text

    # -----------------------------------
    # STEP 3: CREATE POST WITH IMAGE
    # -----------------------------------
    post_url = "https://api.linkedin.com/v2/ugcPosts"

    post_payload = {
        "author": f"urn:li:person:{person_urn}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text
                },
                "shareMediaCategory": "IMAGE",
                "media": [
                    {
                        "status": "READY",
                        "description": {
                            "text": text
                        },
                        "media": asset,
                        "title": {
                            "text": "Image"
                        }
                    }
                ]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    post_response = requests.post(
        post_url,
        headers=headers,
        json=post_payload
    )

    return post_response.status_code, post_response.text