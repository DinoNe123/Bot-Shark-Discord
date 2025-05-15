import discord
from discord.ext import commands
from discord.ui import View, Button
from datetime import timedelta
import random
import asyncio
OWNER_ID = 660507549442900009  # Thay bằng ID Discord của bạn


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='', intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập với tên: {bot.user}")

@bot.command()
async def YeuBe(ctx):
    await ctx.send(f'Yêu {ctx.author.mention} Nhất Server Discord Này <3')

class PunishmentView(View):
    def __init__(self, member: discord.Member, author: discord.Member):
        super().__init__(timeout=60)
        self.member = member
        self.author = author

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.author:
            await interaction.response.send_message("❌ Bạn không có quyền sử dụng bảng này!", ephemeral=True)
            return False
        return True

    # --- Hành động hình phạt ---
    @discord.ui.button(label="Kick", emoji="🥾", style=discord.ButtonStyle.primary)
    async def kick_button(self, interaction: discord.Interaction, button: Button):
        try:
            await self.member.kick(reason=f"Bị kick bởi {interaction.user}")
            await interaction.response.send_message(f"✅ Đã kick {self.member.mention}", ephemeral=False)
        except Exception as e:
            await interaction.response.send_message(f"❌ Không thể kick: {e}", ephemeral=False)
        await interaction.message.delete()  # 🧹 Xoá menu sau khi dùng

    @discord.ui.button(label="Ban", emoji="🔨", style=discord.ButtonStyle.danger)
    async def ban_button(self, interaction: discord.Interaction, button: Button):
        try:
            await self.member.ban(reason=f"Bị ban bởi {interaction.user}")
            await interaction.response.send_message(f"✅ Đã ban {self.member.mention}", ephemeral=False)
        except Exception as e:
            await interaction.response.send_message(f"❌ Không thể ban: {e}", ephemeral=False)
        await interaction.message.delete()  # 🧹 Xoá menu sau khi dùng

    @discord.ui.button(label="Timeout 10 phút", emoji="⏱️", style=discord.ButtonStyle.secondary)
    async def timeout_button(self, interaction: discord.Interaction, button: Button):
        try:
            duration = discord.utils.utcnow() + timedelta(minutes=10)
            await self.member.timeout(until=duration, reason=f"Timeout bởi {interaction.user}")
            await interaction.response.send_message(f"✅ Đã timeout {self.member.mention} trong 10 phút", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Không thể timeout: {e}", ephemeral=True)
        await interaction.message.delete()  # 🧹 Xoá menu sau khi dùng

class KindnessView(View):
    def __init__(self, member: discord.Member, author: discord.Member):
        super().__init__(timeout=60)
        self.member = member
        self.author = author

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.author:
            await interaction.response.send_message("❌ Bạn không có quyền sử dụng bảng này!", ephemeral=True)
            return False
        return True

    # --- Hành động thân thiện ---
    @discord.ui.button(label="Xoa đầu", emoji="🤗", style=discord.ButtonStyle.success)
    async def pat_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(f"{interaction.user.mention} xoa đầu {self.member.mention} một cách dịu dàng 🤗", ephemeral=False)
        await interaction.message.delete()  # 🧹 Xoá menu sau khi dùng

    @discord.ui.button(label="Tặng nhẫn", emoji="💍", style=discord.ButtonStyle.success)
    async def ring_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(f"{interaction.user.mention} đã tặng nhẫn cho {self.member.mention} 💍💖", ephemeral=False)
        await interaction.message.delete()  # 🧹 Xoá menu sau khi dùng

    @discord.ui.button(label="Tặng hoa", emoji="🌹", style=discord.ButtonStyle.success)
    async def flower_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(f"{interaction.user.mention} đã gửi một bông hoa 🌹 đến {self.member.mention}", ephemeral=False)
        await interaction.message.delete()  # 🧹 Xoá menu sau khi dùng

    @discord.ui.button(label="Chích Điện", emoji="⚡", style=discord.ButtonStyle.danger)
    async def lightning_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(f"{interaction.user.mention} đã dùng công cụ chích điện ⚡ đến chết {self.member.mention} rã rời cơ thể không thể di chuyển 💀", ephemeral=False)
        await interaction.message.delete()  # 🧹 Xoá menu sau khi dùng

    @discord.ui.button(label="Bóp Cổ", emoji="😈", style=discord.ButtonStyle.danger)
    async def devil_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(f"{interaction.user.mention} đã lao đến bên cạnh {self.member.mention} nắm cổ và bóp vô cùng dã man!", ephemeral=False)
        await interaction.message.delete()  # 🧹 Xoá menu sau khi dùng


# Lệnh riêng cho chế độ thân thiện
@bot.command()
async def tratan(ctx, member: discord.Member):
    """Lệnh này chỉ hiển thị các hành động thân thiện"""
    embed = discord.Embed(
        title="💖 Chế độ Thân thiện 😈",
        description=f"Bạn có thể thực hiện các hành động đầy mến yêu với {member.mention}!",
        color=discord.Color.green()
    )
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)

    # Tạo view và thêm các nút hành động thân thiện
    view = KindnessView(member, ctx.author)

    # Gửi thông điệp cùng với view
    await ctx.send(embed=embed, view=view)

@bot.command()
@commands.has_permissions(kick_members=True, ban_members=True)
async def check(ctx, member: discord.Member):
    """Lệnh check sẽ chỉ hiển thị các hành động hình phạt mà không có hành động thân thiện."""
    
    # Lấy thời gian gia nhập server của member
    joined_at = member.joined_at.strftime("%d/%m/%Y %H:%M:%S")

    # Tạo một embed chứa thông tin của member
    embed = discord.Embed(
        title="📋 DANH SÁCH HÌNH PHẠT",
        description=f"{member.mention} đang được kiểm tra...",
        color=discord.Color.orange()
    )
    embed.add_field(name="🕒 Tham gia server lúc", value=joined_at, inline=False)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    
    # Tạo view cho chế độ hình phạt
    view = PunishmentView(member, ctx.author)  # Chỉ cần sử dụng một instance của PunishmentView
    await ctx.send(embed=embed, view=view)

class OwnerKindnessView(View):
    def __init__(self, member: discord.Member):
        super().__init__(timeout=60)
        self.member = member

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("❌ Bạn không phải là Owner.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Cắt Cu (Owner)", emoji="🍴", style=discord.ButtonStyle.danger)
    async def cook_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(f"👑 {interaction.user.mention} đã cởi quần {self.member.mention} ra và cắt cu dã man!", ephemeral=False)
        await interaction.message.delete()

@bot.command()
async def owner_tratan(ctx, member: discord.Member):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Lệnh này chỉ dành cho Owner.")
        return

    embed = discord.Embed(title="👑 Menu riêng của Owner", description="Hành động thân thiện bí mật :3", color=discord.Color.gold())
    view = OwnerKindnessView(member)
    await ctx.send(embed=embed, view=view)

@bot.command()
async def soigay(ctx, member: discord.Member = None):
    target = member or ctx.author  # nếu không tag ai thì tự soi chính mình

    percent = random.randint(0, 100)

    # Thanh mức độ (gồm 20 khối, mỗi khối = 5%)
    bar_count = int(percent / 5)
    bar = "█" * bar_count + "░" * (20 - bar_count)

    # Nhận xét (tùy chỉnh thêm)
    if percent >= 80:
        note = "Gay level vô cực 🌈✨"
    elif percent >= 50:
        note = "Có dấu hiệu hơi lệch... 🤨"
    elif percent >= 20:
        note = "Không hề có dấu hiệu lệch phương 😎"
    else:
        note = "Rất chi là thẳng, yên tâm 😏"

    embed = discord.Embed(
        title="🏳️‍🌈 Máy đo độ gay 🏳️‍🌈",
        description=f"Kết quả của {target.mention}",
        color=discord.Color.purple()
    )
    embed.add_field(name="Kết quả", value=f"{percent}%", inline=False)
    embed.add_field(name="Mức độ", value=bar, inline=False)
    embed.add_field(name="Nhận xét", value=note, inline=False)
    embed.set_thumbnail(url=target.avatar.url if target.avatar else target.default_avatar.url)

    await ctx.send(embed=embed)

@bot.command()
async def soidonung(ctx, member: discord.Member = None):
    import random
    target = member or ctx.author

    percent = random.randint(0, 100)
    bar_count = int(percent / 5)
    bar = "█" * bar_count + "░" * (20 - bar_count)

    # Nhận xét vui vui, bạn có thể chỉnh lại
    if percent >= 80:
        note = "Cảnh báo: độ nứng vượt giới hạn 🔥😳"
    elif percent >= 50:
        note = "Hơi bị... thèm đó nha 👀"
    elif percent >= 20:
        note = "Chắc chỉ là tò mò thôi 🐸"
    else:
        note = "Lành mạnh, không rung động 🧘‍♂️"

    embed = discord.Embed(
        title="💦 Máy đo độ nứng 💦",
        description=f"Kết quả của **{target.display_name}**",
        color=discord.Color.red()
    )
    embed.add_field(name="**Kết quả**", value=f"{percent}%", inline=False)
    embed.add_field(name="**Mức độ**", value=bar, inline=False)
    embed.add_field(name="**Nhận xét**", value=note, inline=False)
    embed.set_thumbnail(url=target.avatar.url if target.avatar else target.default_avatar.url)

    await ctx.send(embed=embed)

@bot.command()
async def soiiq(ctx, member: discord.Member = None):
    import random
    target = member or ctx.author

    iq = random.randint(50, 180)  # Giới hạn từ 50 đến 180 cho hợp lý
    bar_count = int((iq - 50) / 6.5)  # Từ 50 đến 180 → 20 khối
    bar = "█" * bar_count + "░" * (20 - bar_count)

    # Nhận xét theo mức IQ
    if iq >= 160:
        note = "Thiên tài vũ trụ 🤯🧠"
    elif iq >= 130:
        note = "Thông minh vượt mức trung bình 📚"
    elif iq >= 90:
        note = "Ổn áp, IQ bình thường 😌"
    elif iq >= 70:
        note = "Hơi ngáo chút xíu 🤪"
    else:
        note = "Cần bật não lên nha 💀"

    embed = discord.Embed(
        title="🧠 Máy đo IQ 🧠",
        description=f"Kết quả của **{target.display_name}**",
        color=discord.Color.blue()
    )
    embed.add_field(name="**Chỉ số IQ**", value=f"{iq}", inline=False)
    embed.add_field(name="**Mức độ**", value=bar, inline=False)
    embed.add_field(name="**Nhận xét**", value=note, inline=False)
    embed.set_thumbnail(url=target.avatar.url if target.avatar else target.default_avatar.url)

    await ctx.send(embed=embed)

@bot.command()
async def soidodam(ctx, member: discord.Member = None):
    import random
    target = member or ctx.author

    percent = random.randint(0, 100)
    bar_count = int(percent / 5)
    bar = "█" * bar_count + "░" * (20 - bar_count)

    # Nhận xét hài hước theo độ "dâm"
    if percent >= 90:
        note = "Cảnh báo đỏ: Dâm thần giáng thế 😳🔥"
    elif percent >= 70:
        note = "Khá là ham... coi chừng nghen 😏"
    elif percent >= 40:
        note = "Có chút gì đó... không trong sáng 👀"
    elif percent >= 20:
        note = "Còn kiểm soát được 😌"
    else:
        note = "Tâm hồn sạch như nước suối 💧😇"

    embed = discord.Embed(
        title="🍑 Máy đo độ dâm 🍑",
        description=f"Kết quả của **{target.display_name}**",
        color=discord.Color.magenta()
    )
    embed.add_field(name="**Kết quả**", value=f"{percent}%", inline=False)
    embed.add_field(name="**Mức độ**", value=bar, inline=False)
    embed.add_field(name="**Nhận xét**", value=note, inline=False)
    embed.set_thumbnail(url=target.avatar.url if target.avatar else target.default_avatar.url)

    await ctx.send(embed=embed)

@bot.command()
async def soidocac(ctx, member: discord.Member = None):
    import random
    target = member or ctx.author

    percent = random.randint(0, 100)
    bar_count = int(percent / 5)
    bar = "█" * bar_count + "░" * (20 - bar_count)

    # Nhận xét độ "dài"
    if percent >= 90:
        note = "Quá khủng... bác sĩ không khâu lại nổi 😳🍆"
    elif percent >= 70:
        note = "Khá dài... phải cuộn lại khi đi tắm 🫣"
    elif percent >= 50:
        note = "Ổn áp, vừa đủ làm người khác ấn tượng 😏"
    elif percent >= 30:
        note = "Cũng ổn... nhưng đừng tự tin quá 😬"
    else:
        note = "Nhỏ nhưng có võ... chắc vậy? 🫠"

    embed = discord.Embed(
        title="🍆 Máy đo độ dài cà tím 🍆",
        description=f"Kết quả của {target.mention}",
        color=discord.Color.purple()
    )
    embed.add_field(name="**Kết quả**", value=f"{percent}%", inline=False)
    embed.add_field(name="**Mức độ**", value=bar, inline=False)
    embed.add_field(name="**Nhận xét**", value=note, inline=False)
    embed.set_thumbnail(url=target.avatar.url if target.avatar else target.default_avatar.url)

    await ctx.send(embed=embed)

@bot.command()
async def soichieucao(ctx, member: discord.Member = None):
    import random
    target = member or ctx.author

    # Random chiều cao (cm), có thể điều chỉnh giới hạn tùy độ troll
    height = random.randint(120, 210)

    # Tạo thanh chiều cao 20 khối (mỗi khối = 4.5cm)
    bar_count = int((height - 120) / 4.5)
    bar = "█" * bar_count + "░" * (20 - bar_count)

    # Nhận xét hài hước
    if height >= 190:
        note = "Chiều cao model, chuẩn bị đi làm người mẫu! 😎"
    elif height >= 170:
        note = "Khá cao đó nha, chuẩn đẹp trai/đẹp gái! 🔥"
    elif height >= 150:
        note = "Tầm trung, đáng yêu phết 😄"
    else:
        note = "Mini size dễ thương quá trời 🥺✨"

    embed = discord.Embed(
        title="📏 Máy đo chiều cao 📏",
        description=f"Kết quả của **{target.display_name}**",
        color=discord.Color.green()
    )
    embed.add_field(name="**Chiều cao**", value=f"{height} cm", inline=False)
    embed.add_field(name="**Mức độ**", value=bar, inline=False)
    embed.add_field(name="**Nhận xét**", value=note, inline=False)
    embed.set_thumbnail(url=target.avatar.url if target.avatar else target.default_avatar.url)

    await ctx.send(embed=embed)

@bot.command()
async def soingoaitinh(ctx, member: discord.Member = None):
    import random
    target = member or ctx.author

    percent = random.randint(0, 100)
    bar_count = int(percent / 5)
    bar = "█" * bar_count + "░" * (20 - bar_count)

    # Nhận xét tùy độ "nguy hiểm"
    if percent >= 90:
        note = "Chuẩn bad boy/girl quốc dân 💔🚨"
    elif percent >= 70:
        note = "Cực kỳ đáng nghi, nên theo dõi 😏"
    elif percent >= 40:
        note = "Có chút lươn lẹo, hơi đáng ngờ 👀"
    elif percent >= 20:
        note = "Khá chung thủy, nhưng ai biết được 😅"
    else:
        note = "Chung thủy như cún con 🐶💘"

    embed = discord.Embed(
        title="💔 Máy soi khả năng ngoại tình 💔",
        description=f"Kết quả của **{target.display_name}**",
        color=discord.Color.red()
    )
    embed.add_field(name="**Tỷ lệ ngoại tình**", value=f"{percent}%", inline=False)
    embed.add_field(name="**Mức độ**", value=bar, inline=False)
    embed.add_field(name="**Nhận xét**", value=note, inline=False)
    embed.set_thumbnail(url=target.avatar.url if target.avatar else target.default_avatar.url)

    await ctx.send(embed=embed)

@bot.command()
async def soisigma(ctx, member: discord.Member = None):
    import random
    target = member or ctx.author

    percent = random.randint(0, 100)
    bar_count = int(percent / 5)
    bar = "█" * bar_count + "░" * (20 - bar_count)

    # Nhận xét chất ngầu
    if percent >= 90:
        note = "Đỉnh của chóp. Không ai điều khiển được bạn 😤🕶️"
    elif percent >= 70:
        note = "Cực kỳ sigma, ít nói, lạnh lùng chuẩn bài 😎"
    elif percent >= 50:
        note = "Cũng có tí sigma, chưa phải tách biệt xã hội 🤔"
    elif percent >= 30:
        note = "Năng lượng sigma hơi yếu... cần thêm gym 💪"
    else:
        note = "Sigma fake rồi, đi làm bài tập lẹ đi 🫠"

    embed = discord.Embed(
        title="🕶️ Máy đo độ Sigma 🕶️",
        description=f"Kết quả của **{target.display_name}**",
        color=discord.Color.dark_grey()
    )
    embed.add_field(name="**Độ Sigma**", value=f"{percent}%", inline=False)
    embed.add_field(name="**Mức độ**", value=bar, inline=False)
    embed.add_field(name="**Nhận xét**", value=note, inline=False)
    embed.set_thumbnail(url=target.avatar.url if target.avatar else target.default_avatar.url)

    await ctx.send(embed=embed)

@bot.command()
async def soitramcam(ctx, member: discord.Member = None):
    import random
    target = member or ctx.author

    percent = random.randint(0, 100)
    bar_count = int(percent / 5)
    bar = "█" * bar_count + "░" * (20 - bar_count)

    # Nhận xét theo độ trầm cảm
    if percent >= 90:
        note = "Tình trạng đáng báo động 😔 Bạn nên tâm sự với người thân hoặc tìm đến chuyên gia."
    elif percent >= 70:
        note = "Dấu hiệu trầm cảm rõ rệt 😟 Hãy chăm sóc bản thân và đừng ngại chia sẻ."
    elif percent >= 50:
        note = "Có vẻ bạn đang trải qua thời gian khó khăn 😕 Hãy nghỉ ngơi và tìm điều tích cực."
    elif percent >= 30:
        note = "Một chút u ám, nhưng bạn vẫn ổn 😊 Cố lên!"
    else:
        note = "Tinh thần ổn định, tiếp tục lan tỏa năng lượng tích cực nhé! 🌟"

    embed = discord.Embed(
        title="🧠 Máy soi độ Trầm Cảm 🧠",
        description=f"Kết quả của **{target.display_name}**",
        color=discord.Color.blue()
    )
    embed.add_field(name="**Mức độ trầm cảm**", value=f"{percent}%", inline=False)
    embed.add_field(name="**Biểu đồ**", value=bar, inline=False)
    embed.add_field(name="**Nhận xét**", value=note, inline=False)
    embed.set_thumbnail(url=target.avatar.url if target.avatar else target.default_avatar.url)

    await ctx.send(embed=embed)

@bot.command()
async def ghepdoi(ctx, member1: discord.Member, member2: discord.Member):
    percent = random.randint(0, 100)
    bar_count = int(percent / 5)
    bar = "█" * bar_count + "░" * (20 - bar_count)

    # Tạm gửi "đang tính toán"
    calculating = await ctx.send(
        embed=discord.Embed(
            title="🔮 Đang tính toán tình yêu... ❤️",
            description=f"**Độ hợp tạm tính:** {percent}%",
            color=discord.Color.magenta()
        )
    )
    await asyncio.sleep(2)

    # Nhận xét theo % hợp nhau
    if percent >= 90:
        note = "Soulmate – tri kỷ đích thực! 💞"
    elif percent >= 70:
        note = "Rất hợp nhau! Có thể thành một đôi 💑"
    elif percent >= 50:
        note = "Khá hiểu nhau và có nhiều điểm chung 🤝"
    elif percent >= 30:
        note = "Cần thêm thời gian tìm hiểu 🧐"
    else:
        note = "Không hợp lắm... nhưng vẫn có thể làm bạn 😅"

    # Embed kết quả
    embed = discord.Embed(
        title="💘 Kết quả ghép đôi 💘",
        description=f"Chúc mừng {member1.mention} và {member2.mention}",
        color=discord.Color.red()
    )
    embed.add_field(name="**Độ hợp nhau**", value=f"{percent}%", inline=False)
    embed.add_field(name="**Mức độ**", value=bar, inline=False)
    embed.add_field(name="**Nhận xét**", value=note, inline=False)

    # Avatar người đầu
    embed.set_thumbnail(url=member1.avatar.url if member1.avatar else member1.default_avatar.url)

    # Avatar người thứ hai đặt ở phần hình chính (dưới)
    embed.set_image(url=member2.avatar.url if member2.avatar else member2.default_avatar.url)

    # Sửa lại tin nhắn ban đầu
    await calculating.edit(embed=embed)

    # Gửi lời chúc riêng
    await ctx.send("💖 Chúc hai bạn hạnh phúc! 💖")

# Token bot
bot.run('MTExNDU5ODE1MjQ4NjUyNzEyOA.GXax9F.RrL6eePP5tCAYOnTo3opNbW4hvisRHRE7hks4U')