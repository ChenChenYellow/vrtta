The API is deployed on Railway, this is the address https://vrtta-production.up.railway.app

POST /score 
take
{
    "product_name": string,
    "materials": string[],
    "weight_grams": int/float,
    "transport": string,
    "packaging": string
}
return
{
    "product_name": string,
    "sustainbility_score": int/float,
    "rating": string,
    "suggestions": string[]
}
There is an input validation to check if the weight_grams is int or float, else it will return a 401 response.
The scoring logic is: 
    -10 for plastic in materials,
    +10 for aluminium in materials,
    -15 for air in transport,
    +5 for rail/sea in transport,
    +10 for recyclable or biodegradable in packaging
Then, the score is divided by weight_grams to obtain the final score. (less weight, highier score)

The rating logic is:
    A: score > 10 
    B: score > 1
    C: score > 0
    D: score <= 0

If materials contains plastic, the suggestions will append "Avoid use of plastic"
If transport is air, the suggestions will append "Avoid air transport"
If packaging is not recyclable nor biodegradable, the suggestions will append "Use biodegradable or recyclable packaging"

The submission and answer will be saved in a local variable.

There is also unit test implemented.

GET /history
return 
[
    {
        submission: {submission of POST /score},
        answer: {response of POST /score}
    },
    {
        submission: {submission of POST /score},
        answer: {response of POST /score}
    },
    {
        submission: {submission of POST /score},
        answer: {response of POST /score}
    }
]

GET /score-summary
return
{
    total_products: int,
    average_score: float,
    ratings:
    [
        A: int,
        B: int,
        C: int,
        D: int
    ],
    top_issues:
    [
        "Avoid use of plastic": int,
        "Avoid air transport": int,
        "Use biodegradable or recyclable packaging": int
    ]
}