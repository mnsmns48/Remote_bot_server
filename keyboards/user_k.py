from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_first_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=False,
                                    keyboard=[
                                        [KeyboardButton(text='В наличии')],
                                        [KeyboardButton(text='Под заказ')],
                                        [KeyboardButton(text='Услуги')],
                                    ])
catalog_full_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                                      one_time_keyboard=False,
                                      keyboard=[
                                          [KeyboardButton(text='Смартфоны')],
                                          [KeyboardButton(text='Планшеты')],
                                          [KeyboardButton(text='Умные часы')],
                                          [KeyboardButton(text='Кнопочные телефоны')],
                                          [KeyboardButton(text='PowerBanks')],
                                          [KeyboardButton(text='Перейти в начало')],
                                      ])
catalog_brand_phones_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                                              one_time_keyboard=False,
                                              keyboard=[
                                                  [KeyboardButton(text='Xiaomi / Redmi / Poco')],
                                                  [KeyboardButton(text='Realme / Oppo / OnePlus')],
                                                  [KeyboardButton(text='Huawei / Honor')],
                                                  [KeyboardButton(text='Samsung')],
                                                  [KeyboardButton(text='Tecno / Infinix')],
                                                  [KeyboardButton(text='TCL')],
                                                  [KeyboardButton(text='Полный список смартфонов')],
                                                  [KeyboardButton(text='Перейти в начало')]
                                              ])

catalog_order_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                                       one_time_keyboard=False,
                                       keyboard=[
                                           [KeyboardButton(text='Apple под заказ')],
                                           [KeyboardButton(text='Xiaomi под заказ')],
                                           [KeyboardButton(text='Samsung под заказ')],
                                           [KeyboardButton(text='Перейти в начало')],
                                       ])
