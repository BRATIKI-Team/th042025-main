from aiogram import Router, F
from aiogram.types import CallbackQuery


router = Router()


@router.callback_query(F.data == "manage_bot")
async def manage_bot(callback: CallbackQuery):
    page = int(callback.data.split("_")[1]) if len(callback.data.split("_")) != 1 else 1
