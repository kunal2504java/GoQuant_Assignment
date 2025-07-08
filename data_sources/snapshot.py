# goquant_assignment/data_sources/snapshot.py

import requests
import json
from typing import List, Dict, Any

# Using the URL that has been confirmed to work.
API_URL = "https://hub.snapshot.org/graphql"

# The production-ready query. It takes a space_id and finds the most
# recently closed proposals, which is ideal for our timeline.
PROPOSALS_QUERY = """
query Proposals($space_id: String!) {
  proposals(
    first: 5,
    skip: 0,
    where: {
      space: $space_id,
      state: "closed"
    },
    orderBy: "created",
    orderDirection: desc
  ) {
    id
    title
    body
    start
    end
    state
    author
  }
}
"""

def get_proposals(space_id: str) -> List[Dict[str, Any]]:
    """
    Fetches the 5 most recent closed proposals for a given Snapshot space.
    """
    print(f"\n--- Fetching proposals for space: {space_id} ---")
    
    json_payload = {
        "query": PROPOSALS_QUERY,
        "variables": {
            "space_id": space_id
        }
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, json=json_payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if 'errors' in data:
            raise ValueError(f"GraphQL error in Snapshot response: {data['errors']}")
        
        proposals = data.get('data', {}).get('proposals')

        if proposals is None:
            raise ValueError(f"Could not find 'proposals' in Snapshot response for '{space_id}'.")

        print(f"--- SUCCESS: Found {len(proposals)} proposals. ---")
        return proposals

    except requests.exceptions.RequestException as e:
        print(f"--- NETWORK ERROR: {e} ---")
        raise
    except (ValueError, KeyError) as e:
        print(f"--- PARSING ERROR: {e} ---")
        raise ValueError(f"Could not parse proposals for '{space_id}'. Reason: {e}") from e
