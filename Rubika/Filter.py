from Rubika.Create_Update import Main_Update
import re
from Rubika.FinitState import state
from Rubika.Config_Logger import bot_logger

class Combine:
    def __init__(self, *args):
        self.list_filter_object = []
        for i in args:
            self.list_filter_object.append(i)

    def __and__(self, other):
        if isinstance(other, Combine):
            new_combine = Combine(*self.list_filter_object, *other.list_filter_object)
        else:
            if isinstance(other, state):
                bot_logger.error(msg="Please use StateFilter for state objects")
                raise ValueError("Please use StateFilter for state objects")
            new_combine = Combine(*self.list_filter_object, other)
        return new_combine

    def checker(self, update_object):
        for x in self.list_filter_object:
            if not x.checker(update_object=update_object):
                return False
        return True

class Text:
    """
    ## کلاس فیلتر کلمات
    ### این فیلتر برای بررسی متن پیام استفاده میشود
    - ### آرگومان ها :
      - `*args` (**str**): یک یا چند رشته که باید با متن مطابقت داشته باشد (مطابقت دقیق) .
      - `for_type` (**str, default = 'new'**): نوع آپدیت‌هایی که این فیلتر روی آن‌ها اعمال می‌شود.
        - به صورت کلی دو مقدار میگیرد(**new , update**)
          - `new` : پیام های جدید
          - `update` : پیام های ویرایش شده
        > **⚠️ مقدار پیش فرض همان `new` است ⚠️**
    - ### توضیح :
      - **این فیلتر متن پیام را با رشته هایی که شما دادید مقایسه میکند و در صورت برابر بودن `True` بر میگرداند.**
    """
    def __init__(self,*args:str,for_type:str="new"):
        self.txt = []
        self.t_update = for_type
        for t in args:
            if isinstance(t, str):
                self.txt.append(t)

    def __and__(self,other):
        if isinstance(other , state):
            bot_logger.error(msg="Please use StateFilter for state objects")
            raise ValueError("Please use StateFilter for state objects")
        return Combine(self,other)

    def checker(self, update_object: Main_Update):
        allowed = {("NewMessage", "new"), ("UpdatedMessage", "update")}
        if (update_object.type_update, self.t_update) not in allowed:
            return False
        t = update_object.message.text
        return t is not None and t in self.txt

class ChatType:
    """
    ## کلاس فیلتر نوع چت
    ### این فیلتر برای تعیین نوع چتی که آپدیت از آن ارسال شده استفاده میشود
    > #### نکته ⚠️ :
    > #### بهتر است در کنار تمام فیلتر هایی که استفاده میکنید این فیلتر را هم با `&` استفاده کنید
    > #### تا گروه ها و کانال ها و چت های خصوصی از هم جدا در نظر گرفته شوند
    >> #### `@Bot_Object.message(Text("kcex") & ChatType("User")) ...`
    - ### آرگومان ها :
      - `*args` (**str**): چهار نوع رشته به عنوان ورودی میگیرد
        - `User` ,`Bot` ,`Group` ,`Channel`
    """
    def __init__(self,*args:str):
        self.chat_type = []
        self.type_list = [
            "User","Bot","Group","Channel"
        ]
        for t in args:
            if t not in self.type_list:
                bot_logger.error(msg="Please Enter Currect argument for ChatType Filter.")
                raise TypeError("Please Enter Currect argument for ChatType Filter.")
            self.chat_type.append(t)

    def __and__(self,other):
        if isinstance(other , state):
            bot_logger.error(msg="Please use StateFilter for state objects")
            raise ValueError("Please use StateFilter for state objects")
        return Combine(self,other)

    def checker(self,update_object:Main_Update):
        return update_object.chat_type is not None and update_object.chat_type in self.chat_type



class Reg:
    """
    ## کلاس فیلتر بر اساس قواعد منظم
    ### این فیلتر برای تطابق متن پیام با یک الگوی regex استفاده می‌شود.
    - ### آرگومان ها :
      - `reg_method` (**تابع**): باید تابعی از ماژول `re` باشد مانند `re.search`، `re.match`، `re.fullmatch`.
      - `pattern` (**str**): الگوی regex.
      - `flag` (**int, default=0**): پرچم‌های regex مانند `re.IGNORECASE`.
      - `for_type` (**str, default='new'**): مانند فیلتر `Text`.
    - ### مثال :
    ```python
        import re
        @Bot_Object.message(Reg(re.search, r"\bسلام\b", re.IGNORECASE))
        async def hello_handler(msg: Main_Update, fsm: StateInjection):
            await Bot_Object.send_message_simple(msg.chat_id, txt="سلام به شما هم!")
    ```
    > #### نکته :
    >> #### اگر متن پیام وجود نداشته باشد یا regex تطابق پیدا نکند، False برمی‌گرداند.
    >> #### از flagهای استاندارد ماژول re می‌توان استفاده کرد.

    """
    def __init__(self,reg_method,pattern:str,flag=0,for_type:str="new"):
        if getattr(reg_method, "__module__", None) != "re":
            bot_logger.error(msg="reg_method must be from the 're' module")
            raise ValueError("reg_method must be from the 're' module")
        self.t_update = for_type
        self.reg_func = reg_method
        self.ptr = pattern
        if isinstance(flag,re.RegexFlag):
            self.flg = flag
        else:
            self.flg = 0

    def __and__(self,other):
        if isinstance(other , state):
            bot_logger.error(msg="Please use StateFilter for state objects")
            raise ValueError("Please use StateFilter for state objects")
        return Combine(self,other)

    def checker(self, update_object: Main_Update) -> bool:
        type_match = (update_object.type_update, self.t_update) in {
            ("NewMessage", "new"),
            ("UpdatedMessage", "update")
        }
        if not type_match:
            return False
        text = update_object.message.text
        return bool(text and self.reg_func(pattern=self.ptr, string=text, flags=self.flg))
    
class Documents:
    """
    ## فیلتر پسوند فایل (اسناد، تصاویر، ویدیوها و ...)

    این فیلتر برای بررسی پسوند فایل‌های ارسالی (عکس، فیلم، صدا، سند و...) استفاده می‌شود.

    - ### آرگومان ها :
      - `extension` (**list, optional**): لیستی از پسوندهای مجاز (بدون نقطه) مانند `["jpg", "png"]`. اگر خالی بماند، هیچ پسوندی قبول نمی‌شود.
      - `for_type` (**str, default='new'**): مانند فیلتر `Text`.

    **دسترسی سریع به دسته‌بندی‌ها:**  
    با استفاده از ویژگی‌های زیر می‌توانید فیلتر آماده دسته‌بندی را دریافت کنید:
    - `Document_Object.picture` : پسوندهای تصویری
    - `Document_Object.video` : پسوندهای ویدیویی
    - `Document_Object.voice` : پسوندهای صوتی
    - `Document_Object.document` : پسوندهای سند و آرشیو و ...

    - ### مثال :
    ```python
    @Bot_Object.message(Document_Object.picture)  # هر نوع تصویری
    async def photo_handler(msg: Main_Update, fsm: StateInjection):
        await Bot_Object.send_message_simple(msg.chat_id, "عکس دریافت شد!")

    @Bot_Object.message(Documents(extension=["pdf", "docx"]))  # فقط PDF و DOCX
    async def doc_handler(msg: Main_Update, fsm: StateInjection):
        await Bot_Object.send_message_simple(msg.chat_id, "سند دریافت شد.")
    ```
    """
    def __init__(self,extension=None,for_type:str="new"):
        self.mim_dic = {
            "video": ["mp4", "avi", "mov", "wmv", "flv", "mkv", "webm", "m4v", "mpg", "mpeg", "3gp", "ogv", "vob", "ts", "mts"],
            "picture": ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "tif", "svg", "eps", "raw", "cr2",
                         "nef", "arw", "dng", "heic", "heif", "ico", "webp", "psd", "ai", "indd"],
            "voice": ["mp3", "wav", "wma", "aac", "flac", "ogg", "m4a", "opus", "aiff", "alac", "amr", "ape"],
            "document": ["txt", "rtf", "doc", "docx", "odt", "tex", "pdf", "epub", "md", "log", "msg", "wpd", "wps", "pages",
                         "csv", "dat", "db", "dbf", "mdb", "accdb", "sql", "xml", "json", "xls", "xlsx", "ods", "dta", "sav", "rda",
                         "zip", "rar", "7z", "tar", "gz", "bz2", "xz", "z", "cab", "arj", "lzh", "iso", "dmg", "pkg", "deb", "rpm", "apk",
                         "exe", "msi", "app", "bat", "cmd", "com", "bin", "sh", "cgi", "jar", "py", "pyc", "pl", "rb", "class",
                         "html", "htm", "xhtml", "php", "asp", "aspx", "jsp", "css", "scss", "js", "jsx", "ts", "tsx", "json", "xml", "rss",
                         "atom","svg", "ai", "eps", "cdr", "dwg", "dxf", "3ds", "blend", "c4d", "lwo", "obj", "stl", "fbx",
                         "dll", "sys", "drv", "ini", "cfg", "conf", "reg", "log", "tmp", "cache", "swap",
                         "c", "cpp", "h", "java", "py", "rb", "pl", "go", "rs", "swift", "kt", "cs", "php", 
                         "js", "ts", "sql", "r", "m", "scala", "lua", "groovy", "gradle",
                         "ttf", "otf", "woff", "woff2", "eot", "fnt", "fon",
                         "psd", "ai", "indd", "fla", "swf", "pptx", "key", "numbers", "dwg", "sldprt", "step"]
        }
        self.t_update = for_type
        self.selected_extensions = extension or []

    def __and__(self,other):
        if isinstance(other , state):
            bot_logger.error(msg="Please use StateFilter for state objects")
            raise ValueError("Please use StateFilter for state objects")
        return Combine(self,other)
    
    def __getattr__(self, name):
        if name in self.mim_dic:
            return Documents(extension=self.mim_dic[name])
        bot_logger.error(msg=f"Documents has no attribute '{name}'")
        raise AttributeError(f"Documents has no attribute '{name}'")

    def checker(self, update_object):
        type_match = (update_object.type_update, self.t_update) in {
            ("NewMessage", "new"),
            ("UpdatedMessage", "update")
        }
        if not type_match:
            return False
        ext = getattr(update_object.message, "file_extension", None)
        return ext is not None and ext in self.selected_extensions

Document_Object = Documents()

class GeneralFilter:
    """
    ## فیلتر عمومی برای انواع خاص پیام

    ### این فیلتر برای تشخیص آپدیت‌هایی که شامل یک نوع خاص از محتوا هستند (نظرسنجی، موقعیت مکانی، مخاطب، حذف پیام) استفاده می‌شود.

    - ### آرگومان ها :
      - `tp` (**str, optional**): نوع فیلتر که می‌تواند یکی از مقادیر زیر باشد:
        - `"poll"` : نظرسنجی
        - `"location"` : موقعیت مکانی
        - `"contact_message"` : مخاطب
        - `"delete_message"` : پیام حذف شده (این مورد نیاز به `tp` ندارد و با `F.delete_message` فراخوانی می‌شود)
      - `for_type` (**str, default='new'**): مانند فیلتر `Text`.

    **دسترسی سریع:**  
    نمونه آماده `F` دارای ویژگی‌های زیر است:
    - `F.poll` : فیلتر نظرسنجی
    - `F.location` : فیلتر مکان
    - `F.contact_message` : فیلتر مخاطب
    - `F.delete_message` : فیلتر حذف پیام (برای `RemovedMessage`)

    - ### مثال :
    ```python

        @Bot_Object.message(F.poll)
        async def poll_handler(msg: Main_Update, fsm: StateInjection):
            await Bot_Object.send_message_simple(msg.chat_id, "یک نظرسنجی فرستاده شد!")

        @Bot_Object.message(F.delete_message)
        async def delete_handler(msg: Main_Update, fsm: StateInjection):
            # پیامی حذف شده است
            print(f"پیام {msg.message.removed_message_id} حذف شد.")

    ```
    > #### نکته ها :
    >> #### برای delete_message نوع آپدیت باید "RemovedMessage" باشد<br> و در آن صورت بدون نیاز به بررسی متن، True برمی‌گرداند.
    >> #### برای سایر موارد، وجود attribute مربوطه در update_object.message بررسی می‌شود.

    
    """
    def __init__(self,tp:str=None,for_type:str="new"):
        self.t_update = for_type
        self.type_filter = tp
        self.tp_list = ["poll","location","contact_message","delete_message"]
    def __and__(self,other):
        if isinstance(other , state):
            bot_logger.error(msg="Please use StateFilter for state objects")
            raise ValueError("Please use StateFilter for state objects")
        return Combine(self,other)
    def __getattr__(self, name):
        if name in self.tp_list:
            return GeneralFilter(tp=name)
        bot_logger.error(msg=f"GeneralFilter(F) has no attribute '{name}'")
        raise AttributeError(f"GeneralFilter(F) has no attribute '{name}'")

    def checker(self, update_object):
        valid_pairs = {("NewMessage", "new"), ("UpdatedMessage", "update")}

        if (update_object.type_update, self.t_update) in valid_pairs:
            return bool(getattr(update_object.message, self.type_filter, None))
        
        if update_object.type_update == "RemovedMessage":
            return True
        
        return False
        
    
F = GeneralFilter()

class StateFilter:
    """
    ## فیلتر وضعیت (State) ماشین حالت

    #### این فیلتر بررسی می‌کند که وضعیت جاری کاربر با یک شیء `state` خاص برابر باشد. معمولاً برای کنترل جریان گفتگو استفاده می‌شود.

    - ### آرگومان ها :
      - `State` (**state, default=state()**): شیء state که باید با وضعیت فعلی کاربر مطابقت داشته باشد.
      - `for_type` (**str, default='new'**): مانند فیلتر `Text`.

    - ### مثال :

    ```python
    from Rubika import state_group, state

    class MyStates(state_group):
        START = state()
        WAITING_NAME = state()
        WAITING_AGE = state()

    @Bot_Object.message(Text("start") & StateFilter(MyStates.START))
    async def start_cmd(msg: Main_Update, fsm: StateInjection):
        await fsm.set_state(MyStates.WAITING_NAME)
        await Bot_Object.send_message_simple(msg.chat_id, "نام خود را وارد کنید:")

    @Bot_Object.message(StateFilter(MyStates.WAITING_NAME))
    async def get_name(msg: Main_Update, fsm: StateInjection):
        name = msg.message.text
        await fsm.set_state(MyStates.WAITING_AGE, data={"name": name})
        await Bot_Object.send_message_simple(msg.chat_id, f"خوش آمدید {name}، سن خود را وارد کنید:")
    ```
    > #### نکته :
    >> #### برای کار با stateها حتماً از state_group استفاده کنید تا به طور خودکار next و previous تنظیم شوند.
    
    """
    def __init__(self,State:state=state(),for_type:str="new"):
        self.object_state = State
        self.t_update = for_type

    def __and__(self,other):
        if isinstance(other , state):
            bot_logger.error(msg="Please use StateFilter for state objects")
            raise ValueError("Please use StateFilter for state objects")
        return Combine(self,other)
    
    def checker(self, update_object: Main_Update) -> bool:
        type_match = (update_object.type_update, self.t_update) in {
            ("NewMessage", "new"),
            ("UpdatedMessage", "update")
        }
        if not type_match:
            return False
        return update_object.UserState == self.object_state
