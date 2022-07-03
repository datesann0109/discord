import discord
import yaml

# 自由に参加してほしくないチャンネル
# すでに自由に参加できるチャンネルも登録しておくとわざわざ表示されない
VOID_CHANNELS = ['チャンネル管理', '雑談', '暇人', '人狼']

with open('./setting.yaml') as f:  # 設定ファイルの読み込み
    setting = yaml.safe_load(f)

BOT_TOKEN = setting['BOT_TOKEN']  # BOTのトークン
CHANNEL_ID = setting['CHANNEL_ID']  # BOTが動作するチャンネルのID


client = discord.Client()


# discordのBOTが正常に起動した時
@client.event
async def on_ready():
    print('Bot Start!')
    # チャンネル指定
    main_channel = client.get_channel(CHANNEL_ID)
    # main_channelの内容をすべて消す
    await main_channel.purge()
    # 送信するメッセージの作成
    message = "-------チャンネル一覧-------\n"
    for channel in main_channel.guild.text_channels:
        if channel.name not in VOID_CHANNELS:
            message += f"{channel.name}\n"

    # 操作説明
    message += """
-------コマンド-------
チャンネルに参加\t/join チャンネル名
チャンネルの作成\t/create チャンネル名
    """

    # messageをdiscordに表示
    await main_channel.send(message)
    print('waiting for command')


@client.event
async def on_message(message):
    # 指定したチャネル以外では動作しないように
    if message.channel.id != CHANNEL_ID:
        return

    # BOTのメッセージを無視
    if message.author.bot:
        return

    # チャンネルへの参加処理
    order = '/join'
    order += ' '  # コマンドの後ろにスペースが必ず入っているように
    if order == str(message.content)[:len(order)]:
        # 参加したいチャンネル名を取得
        search_channel = message.content[len(order):]
        member = message.author

        if search_channel not in VOID_CHANNELS:
            channel = discord.utils.get(
                message.guild.text_channels, name=search_channel)
            if channel is not None:
                await channel.set_permissions(member, read_messages=True)
                await channel.send(f"{member}が参加しました.")
                print(f"{channel}に{member}が参加しました.")
            else:
                # 存在しないチャンネルに参加しようとした時
                await member.send(f"{search_channel}というチャンネルは存在しません.")
                print(f"{member}が存在しない{search_channel}へ参加しようとしました.")
        else:
            # VOID_CHANNELSに登録したチャンネルに参加しようとした時
            await member.send(f"{search_channel}チャンネルへの参加に失敗しました.")
            print(f"{member}が権限のない{search_channel}へ参加しようとしました.")

    await message.delete()

client.run(BOT_TOKEN)
