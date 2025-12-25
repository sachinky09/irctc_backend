from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from irctc_backend.mongo import mongo_collection

class TopRoutesView(APIView):
    permission_classes = [permissions.IsAdminUser] 

    def get(self, request):
     
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "source": "$params.source",
                        "destination": "$params.destination"
                    },
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ]

        results = list(mongo_collection.aggregate(pipeline))

      
        top_routes = [
            {
                "source": r["_id"]["source"],
                "destination": r["_id"]["destination"],
                "search_count": r["count"]
            }
            for r in results
        ]

        return Response({"top_routes": top_routes}, status=status.HTTP_200_OK)
