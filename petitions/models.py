from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Petition(models.Model):
    movie_title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='petitions_created')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.movie_title

class PetitionVote(models.Model):
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE, related_name='votes')
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='petition_votes')
    # We only need affirmative votes for this user story
    vote = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('petition', 'voter')  # prevent multiple votes by same user

    def __str__(self):
        return f"{self.voter} voted YES on {self.petition}"
