from rest_framework import serializers

from ..models import Ad, ExchangeProposal


class AdSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Ad
        fields = [
            'id', 'user', 'title', 'description', 'image_url', 'category', 
            'condition', 'created_at',
        ]
        read_only_fields = ['id', 'user', 'created_at']


class ExchangeProposalSerializer(serializers.ModelSerializer):
    ad_sender_id = serializers.IntegerField(write_only=True)
    ad_receiver_id = serializers.IntegerField(write_only=True)
    ad_sender = AdSerializer(read_only=True)
    ad_receiver = AdSerializer(read_only=True)

    class Meta:
        model = ExchangeProposal
        fields = [
            'id', 'ad_sender', 'ad_receiver', 'ad_sender_id', 'ad_receiver_id', 
            'comment', 'status', 'created_at',
        ]
        read_only_fields = ['id', 'status', 'created_at']

    def create(self, validated_data):
        sender_id = validated_data.pop('ad_sender_id')
        receiver_id = validated_data.pop('ad_receiver_id')
        proposal = ExchangeProposal.objects.create(
            ad_sender_id=sender_id,
            ad_receiver_id=receiver_id,
            status='pending',
            **validated_data
        )
        return proposal


class ExchangeProposalSerializer(serializers.ModelSerializer):
    ad_sender = serializers.PrimaryKeyRelatedField(queryset=Ad.objects.all())
    ad_receiver = serializers.PrimaryKeyRelatedField(queryset=Ad.objects.all())

    class Meta:
        model = ExchangeProposal
        fields = [
            'id', 'ad_sender', 'ad_receiver', 'comment', 'status', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'status': {'read_only': True},
        }
