import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
INTRO_CHANNEL_ID_STR = os.getenv('INTRO_CHANNEL_ID', '0')
CUSTOM_EMOJI = os.getenv('CUSTOM_EMOJI', '📝')

# Validasi TOKEN
if not TOKEN:
    print("❌ ERROR: DISCORD_TOKEN tidak ditemukan!")
    print("Set DISCORD_TOKEN di environment variables atau di .env file")
    exit()

try:
    INTRO_CHANNEL_ID = int(INTRO_CHANNEL_ID_STR)
except ValueError:
    print("❌ ERROR: INTRO_CHANNEL_ID harus berupa angka!")
    exit()

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionary untuk simpan message ID intro per channel
last_intro_messages = {}

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'{bot.user} has connected to Discord!')

class IntroModal(discord.ui.Modal):
    def __init__(self, channel: discord.TextChannel, age_group: str, user: discord.User):
        super().__init__(title="📝 Form Intro Kamu")
        self.channel = channel
        self.age_group = age_group
        self.user = user
        
        self.name = discord.ui.TextInput(
            label="Nama Kamu",
            placeholder="Masukkan nama panggilan...",
            required=True,
            max_length=100
        )
        self.add_item(self.name)
        
        self.hobbies = discord.ui.TextInput(
            label="Hobby",
            placeholder="Masukkan hobby mu...",
            required=True,
            max_length=200
        )
        self.add_item(self.hobbies)
        
        self.about = discord.ui.TextInput(
            label="Tentang Kamu",
            placeholder="Ceritain tentang dirimu (opsional)...",
            required=False,
            max_length=1000
        )
        self.add_item(self.about)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            # Embed yang lebih cantik dengan dark theme
            embed = discord.Embed(
                title=f"✨ {self.name.value}",
                description="Halo! Selamat datang di Mickey Trap Academy 👋",
                color=discord.Color.from_rgb(45, 45, 65)
            )
            
            # Add fields dengan formatting yang lebih bagus
            embed.add_field(
                name="👤 Nama",
                value=f"```{self.name.value}```",
                inline=True
            )
            embed.add_field(
                name="🎂 Umur",
                value=f"```{self.age_group}```",
                inline=True
            )
            
            embed.add_field(
                name="🎮 Hobby",
                value=f"```{self.hobbies.value}```",
                inline=False
            )
            
            if self.about.value:
                embed.add_field(
                    name="📝 Tentang Saya",
                    value=f"```{self.about.value}```",
                    inline=False
                )
            
            embed.set_thumbnail(url=self.user.avatar.url)
            embed.set_footer(
                text=f"Intro dari {self.user} • {discord.utils.utcnow().strftime('%d/%m/%Y')}",
                icon_url=self.user.avatar.url
            )
            
            # Defer interaction
            await interaction.response.defer()
            
            # Hapus pesan intro yang lama jika ada
            channel_id = self.channel.id
            if channel_id in last_intro_messages:
                try:
                    old_message = await self.channel.fetch_message(last_intro_messages[channel_id])
                    await old_message.delete()
                except:
                    pass
            
            # Post biodata user
            await self.channel.send(embed=embed)
            
            # Post ulang pesan intro yang baru
            intro_embed = discord.Embed(
                title="📝 Intro Member Baru",
                description="Silakan klik tombol di bawah untuk mengisi form intro kamu!",
                color=discord.Color.from_rgb(45, 45, 65)
            )
            intro_embed.add_field(
                name="📋 Form terdiri dari:",
                value="• Nama panggilan\n• Umur\n• Hobby\n• Tentang dirimu (opsional)",
                inline=False
            )
            intro_embed.add_field(
                name="💡 Tips",
                value="Isi dengan jujur dan menarik agar member lain tertarik berkenalan!",
                inline=False
            )
            
            view = IntroButtonView(self.channel)
            new_intro_msg = await self.channel.send(embed=intro_embed, view=view)
            
            # Simpan message ID yang baru
            last_intro_messages[channel_id] = new_intro_msg.id
            
        except Exception as e:
            print(f"Error in on_submit: {e}")
            try:
                await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)
            except:
                pass

class AgeSelectView(discord.ui.View):
    def __init__(self, channel: discord.TextChannel):
        super().__init__(timeout=300)
        self.channel = channel

    @discord.ui.select(
        placeholder="Pilih umur mu...",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label="< 18 tahun",
                value="<18",
            ),
            discord.SelectOption(
                label="18+ Tahun",
                value="18+",
            ),
        ]
    )
    async def age_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        age_selected = select.values[0]
        modal = IntroModal(self.channel, age_selected, interaction.user)
        
        # Send modal dulu
        await interaction.response.send_modal(modal)
        
        # Hapus message dropdown setelah 0.5 detik
        try:
            await interaction.delete_original_response()
        except:
            pass

class IntroButtonView(discord.ui.View):
    def __init__(self, channel: discord.TextChannel):
        super().__init__(timeout=None)
        self.channel = channel
    
    @discord.ui.button(label="Isi Intro", style=discord.ButtonStyle.primary, emoji="📝")
    async def intro_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Buat embed yang muncul seperti modal - dark theme
        embed = discord.Embed(
            title="📝 Pilih Kelompok Umur",
            description="Silakan pilih kelompok umur kamu di bawah:",
            color=discord.Color.from_rgb(45, 45, 65)
        )
        
        view = AgeSelectView(self.channel)
        await interaction.response.send_message(
            embed=embed,
            view=view,
            ephemeral=True
        )

@bot.tree.command(name="intro", description="Buat pesan intro di channel!")
async def intro(interaction: discord.Interaction):
    # Get intro channel
    if INTRO_CHANNEL_ID == 0:
        await interaction.response.send_message(
            "❌ Channel intro belum di-set. Admin perlu set `INTRO_CHANNEL_ID` di .env",
            ephemeral=True
        )
        return
    
    channel = bot.get_channel(INTRO_CHANNEL_ID)
    if not channel:
        await interaction.response.send_message(
            "❌ Channel intro tidak ditemukan. Cek `INTRO_CHANNEL_ID` di .env",
            ephemeral=True
        )
        return
    
    # Buat embed dengan button - dark theme
    embed = discord.Embed(
        title="📝 Intro Member Baru",
        description="Silakan klik tombol di bawah untuk mengisi form intro kamu!",
        color=discord.Color.from_rgb(45, 45, 65)
    )
    embed.add_field(
        name="📋 Form terdiri dari:",
        value="• Nama panggilan\n• Umur\n• Hobby\n• Tentang dirimu (opsional)",
        inline=False
    )
    embed.add_field(
        name="💡 Tips",
        value="Isi dengan jujur dan menarik agar member lain tertarik berkenalan!",
        inline=False
    )
    
    view = IntroButtonView(channel)
    
    # Send ke channel intro
    intro_msg = await channel.send(embed=embed, view=view)
    
    # Simpan message ID intro
    last_intro_messages[channel.id] = intro_msg.id
    
    # Reply ke user
    await interaction.response.send_message(
        f"✅ Pesan intro sudah di-post ke <#{INTRO_CHANNEL_ID}>!",
        ephemeral=True
    )

bot.run(TOKEN)
