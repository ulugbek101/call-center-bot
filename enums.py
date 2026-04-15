COMMANDS = [
    ("/start", "Botni ishga tushirish"),
    ("/help", "Yordam olish"),
    ("/milestones", "Yutuqlar ro'yxati"),    # TODO: Not implemented
    ("/leaderboard", "Liderlar doskasi"),           # TODO: Not implemented
]


how_to_collect_scores = {
    "kunlik": [
        "+1 ball - 1 kunda 15 mln. so'm lik yetkazib berish",
        "+1 ball - 15 mln. so'mlik buyurtmadan 15 mln. so'm muvaffaqiyat 100%",
        "+0.5 ball - 4 mln. so'mlik qayta xarid",
    ],
    "haftalik": [
        "+0.5 ball - Har hafta 40 mln. so'm muvaffaqiyat",
        "+5 ball - 40 mln. so'mlik savdo qiladigan operator olib kelsa",
        "+0.5 ball - Haftalik qaytarish 10% dan past bo'lsa",
    ],
    "oylik": [
        "+1 ball - 1 oyda 130 mln. so'mlik muvaffaqiyat",
    ]
}

how_to_lose_scores = [
    "-1 ball, agar Mijoz bilan urushsa",
    "-0.5 ball, agar zakaz chopish 15 kunlik zakaz padvejdenya"
]
