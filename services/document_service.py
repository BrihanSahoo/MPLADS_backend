from database.database import supabase




async def get_docs_by_constituency(constituency:str):
    constituency = constituency.upper()
    response = (
        supabase
        .table("mplads_documents")
        .select("*")
        .eq("constituency", constituency)
        .execute()
    )
    
    return {
        "constituency": constituency,
        "data": response.data,
        "count": len(response.data)
    }