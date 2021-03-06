# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-25 06:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pb_analyzer', '0004_auto_20171124_1637'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='gameCreation',
            new_name='game_creation',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='gameDuration',
            new_name='game_duration',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='gameId',
            new_name='game_id',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='gameMode',
            new_name='game_mode',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='gameType',
            new_name='game_type',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='gameVersion',
            new_name='game_version',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='mapId',
            new_name='map_id',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='platformId',
            new_name='platform_id',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='queueId',
            new_name='queue_id',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='seasonId',
            new_name='season_id',
        ),
        migrations.RenameField(
            model_name='participant',
            old_name='championId',
            new_name='champion_id',
        ),
        migrations.RenameField(
            model_name='participant',
            old_name='participantId',
            new_name='participant_id',
        ),
        migrations.RenameField(
            model_name='participant',
            old_name='teamId',
            new_name='team_id',
        ),
        migrations.RenameField(
            model_name='participantidentity',
            old_name='participantId',
            new_name='participant_id',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='accountId',
            new_name='account_id',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='currentAccountId',
            new_name='current_account_id',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='currentPlatformId',
            new_name='current_platformId',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='matchHistoryUri',
            new_name='match_history_uri',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='participantIdentity',
            new_name='participant_identity',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='platformId',
            new_name='platform_id',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='profileIcon',
            new_name='profile_icon',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='summonerId',
            new_name='summoner_id',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='summonerName',
            new_name='summoner_name',
        ),
        migrations.RemoveField(
            model_name='participanttimeline',
            name='participantId',
        ),
    ]
