SELECT p.title,p.content,p.ownner_id AS owner_id,p.id as post_id , COUNT(v.user_id) as LikeCount
FROM posts p
LEFT JOIN votes v
ON p.id = v.post_id
GROUP BY p.ownner_id, p.id,p.title,p.content
ORDER BY p.id,p.ownner_id DESC
