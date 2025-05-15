import os
import csv
import json
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List
from enum import Enum
from openai import OpenAI, APIError

load_dotenv()


CSV_FILE = os.getenv("CSV_FILE", "services.csv")
TAGGED_CSV_FILE = os.getenv("TAGGED_CSV_FILE", "services_tagged.csv")
LLM = os.getenv("LLM")
LLM_HOST = os.getenv("LLM_HOST")
LLM_API_KEY = os.getenv("LLM_API_KEY")


class Services(BaseModel):
    class ServiceWithTags(BaseModel):
        class AllowedTags(str, Enum):
            BEARD_BLOWOUT = "Beard Blowout"
            BEARD_COLORING = "Beard Coloring"
            BEARD_CONDITIONING = "Beard Conditioning"
            BEARD_OIL = "Beard Oil"
            BEARD_SCULPTING = "Beard Sculpting"
            BEARD_TRIM_CLIPPER = "Beard Trim-Clipper/Trimmer"
            BEARD_TRIM_RAZOR = "Beard Trim-Straight-razor"
            BEARD_WASH = "Beard Wash"
            GOATEE_TRIM = "Goatee Trim"
            HEAD_SHAVE = "Head Shave"
            HOT_TOWEL = "Hot Towel"
            LINE_UP = "Line-Up/Edge Up"
            MUSTACHE_TRIM = "Mustache Trim"
            NECK_SHAVE_CLIPPER = "Neck Shave-Clipper/Trimmer"
            NECK_SHAVE_RAZOR = "Neck Shave-Razor"
            BEARD_SHAVE_CLASSIC = "Beard Shave-Classic/Traditional-Razor"
            BEARD_SHAVE_CLIPPER = "Beard Shave-Clipper/Trimmer"

        id: str = Field(
            ...,
            description="Unique identifier for the service.",
        )
        name: str = Field(
            ...,
            description="Name of the service.",
        )
        description: str = Field(
            ...,
            description="Description of the service.",
        )
        price: float = Field(
            ...,
            description="Price of the service.",
        )
        duration_in_minutes: int = Field(
            ...,
            description="Duration of the service in minutes.",
        )
        location_name: str = Field(
            ...,
            description="Name of the location where the service is provided.",
        )
        tags: List[AllowedTags] = Field(
            ...,
            description="Tags suitable to the service.",
        )
    
    services: List[ServiceWithTags] = Field(
        ...,
        description="List of salon services with their information and tags.",
    )


def read_csv():
    with open(CSV_FILE, "r") as csv_file:
        return [row for row in csv.DictReader(csv_file, delimiter=";")]


def write_csv(data):
    with open(TAGGED_CSV_FILE, "w", newline="") as csv_file:
        fieldnames = [
            "id",
            "name",
            "description",
            "price",
            "duration_in_minutes",
            "location_name",
            "tags",
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        for item in data:
            item["tags"] = ", ".join(item["tags"])
            writer.writerow(item)


def tag_csv_using_llm(salon_services):
    client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_HOST)

    messages = [
        {
            "role": "system",
            "content": """You are a helpful assistant that tags salon services with the most relevant tags.
            You will be provided with an array of JSON values that list the services of the salons, each with its name, description, price, duration, and location. Your task is to analyze the services and assign the most relevant tags from the allowed tags.""",
        },
        {
            "role": "user",
            "content": f"""Following is the array of JSON values that list the services of the salons, each with its name, description, price, duration, and location.
            
            ##### SALON SERVICES #####
            {salon_services}""",
        },
    ]

    try:
        response = client.chat.completions.create(
            model=LLM,
            messages=messages,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "service_with_tags",
                    "description": "Salon services with their information and tags.",
                    "schema": Services.model_json_schema(),
                    "strict": True,
                },
            },
        )
    except APIError as e:
        print(f"API error: {e}")
        return None

    result = json.loads(response.choices[0].message.content)
    return result


def main():
    print("Starting the tagging process...")
    salon_services = read_csv()
    tagged_services = tag_csv_using_llm(salon_services)
    if tagged_services:
        write_csv(tagged_services.get("services", []))
        print("Tagging process completed. Tagged services saved to", TAGGED_CSV_FILE)
    else:
        print("Tagging process failed. No tagged services were saved. Try again.")
    
    print("Exiting the program.")


if __name__ == "__main__":
    main()
