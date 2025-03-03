import boto3
from boto3.dynamodb.conditions import Attr
from typing import Optional, Dict, Any
import os


class DynamoHandler:
    def __init__(self):
        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name=os.getenv("AWS_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
        self.table = self.dynamodb.Table("habit-slap-users-dev")

    def get_user(self, email: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.table.get_item(Key={"email": email})
            return response.get("Item")
        except Exception as e:
            print(f"Error getting user: {str(e)}")
            return None

    def create_user(self, user_data: Dict[str, Any]) -> bool:
        try:
            self.table.put_item(Item=user_data)
            return True
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return False

    def update_user(self, email: str, update_data: Dict[str, Any]) -> bool:
        try:
            # Initialize update components
            update_parts = []
            expression_values = {}
            expression_names = {}

            # Build the update expression
            for key, value in update_data.items():
                if key != "email":  # Skip the primary key
                    # Create safe attribute names (replace invalid characters)
                    safe_key = key.replace("-", "_")
                    attr_name = f"#attr_{safe_key}"
                    attr_value = f":val_{safe_key}"

                    update_parts.append(f"{attr_name} = {attr_value}")
                    expression_names[attr_name] = key
                    expression_values[attr_value] = value

            # Combine all parts into the update expression
            update_expression = "SET " + ", ".join(update_parts)

            self.table.update_item(
                Key={"email": email},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
                ExpressionAttributeNames=expression_names,
            )
            return True
        except Exception as e:
            print(f"Error updating user: {str(e)}")
            return False

    def query_by_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.table.scan(
                FilterExpression=Attr("magic_link_token").eq(token)
            )
            items = response.get("Items", [])
            return items[0] if items else None
        except Exception as e:
            print(f"Error querying by token: {str(e)}")
            return None

    def delete_user(self, email: str) -> bool:
        try:
            self.table.delete_item(Key={"email": email})
            return True
        except Exception as e:
            print(f"Error deleting user: {str(e)}")
            return False
