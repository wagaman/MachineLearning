__author__ = 'Administrator'

import pymysql

# 打开数据库连接
db = pymysql.connect("127.0.0.1", "root", "root", "news", charset="utf8")

def db_insert(db, sql, params):
    cursor = db.cursor()
    try:
        # 执行sql语句
        cursor.execute(sql, params)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        # 如果发生错误则回滚
        print(e)
        db.rollback()

def db_fetch_one(db, sql):
    cursor = db.cursor()
    # 执行sql语句
    cursor.execute(sql)
    data = cursor.fetchone()
    return data[0]

sql = "insert into list_zhihu_answer(question_id,question_title,excerpt,id,content,voteup_count,comment_count,updated_time,author_id,author_name,author_headline,author_gender) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
params = (35786685, '有没有像军装一样帅气的服装款式？', '我的公众号「商务范」最近发过一篇<a href="https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMjM5OTY1MDMxMg%3D%3D%26mid%3D402221704%26idx%3D3%26sn%3Da5bc91995ba7bfaa80ac42399d23b2f8%23rd" class=" wrap external" target="_blank" rel="nofollow noreferrer">宋仲基撩妹靠什么？赤裸裸的制服诱惑！<i class="icon-external"></i></a>，可以参考。<strong>范主说：穿军装的汉子才最MAN！</strong><strong>（商务范出品，转载请注明）</strong> 韩剧《太阳的后裔》最近实在是太火啦，据说喜欢看韩剧的女生，现在的老公都是剧中男主宋仲基。范主就想呢，为…', 92189453, '<blockquote>我的公众号「商务范」最近发过一篇<a href="https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMjM5OTY1MDMxMg%3D%3D%26mid%3D402221704%26idx%3D3%26sn%3Da5bc91995ba7bfaa80ac42399d23b2f8%23rd" class=" wrap external" target="_blank" rel="nofollow noreferrer">宋仲基撩妹靠什么？赤裸裸的制服诱惑！<i class="icon-external"></i></a>，可以参考。</blockquote><p><strong>范主说：穿军装的汉子才最MAN！</strong></p><p><strong>（商务范出品，转载请注明）</strong></p><br><p>韩剧《太阳的后裔》最近实在是太火啦，据说喜欢看韩剧的女生，现在的老公都是剧中男主宋仲基。范主就想呢，为什么宋仲基可以把万千少女的心给迷倒？</p><noscript><img src="https://pic4.zhimg.com/ad97b437d1acd3424c0b34c68306b59f_b.jpg" data-rawwidth="639" data-rawheight="427" class="origin_image zh-lightbox-thumb" width="639" data-original="https://pic4.zhimg.com/ad97b437d1acd3424c0b34c68306b59f_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="639" data-rawheight="427" class="origin_image zh-lightbox-thumb lazy" width="639" data-original="https://pic4.zhimg.com/ad97b437d1acd3424c0b34c68306b59f_r.jpg" data-actualsrc="https://pic4.zhimg.com/ad97b437d1acd3424c0b34c68306b59f_b.jpg"><br><br><p>是因为会那美好的肉体么？</p><noscript><img src="https://pic2.zhimg.com/60caa6c23d57c1f8d6865159bb75fc25_b.png" data-rawwidth="263" data-rawheight="198" class="content_image" width="263"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="263" data-rawheight="198" class="content_image lazy" width="263" data-actualsrc="https://pic2.zhimg.com/60caa6c23d57c1f8d6865159bb75fc25_b.png"><br><noscript><img src="https://pic3.zhimg.com/4bfd8cadca2d947a7dfe8433734e941e_b.png" data-rawwidth="265" data-rawheight="186" class="content_image" width="265"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="265" data-rawheight="186" class="content_image lazy" width="265" data-actualsrc="https://pic3.zhimg.com/4bfd8cadca2d947a7dfe8433734e941e_b.png"><br><p>还是因为会对乔妹那深情的眼神：</p><noscript><img src="https://pic1.zhimg.com/f465f23e8ff8b9b398c859e7dc5178a0_b.png" data-rawwidth="379" data-rawheight="375" class="content_image" width="379"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="379" data-rawheight="375" class="content_image lazy" width="379" data-actualsrc="https://pic1.zhimg.com/f465f23e8ff8b9b398c859e7dc5178a0_b.png"><br><p>范主看了好多集，才知道，人家的撩妹技能可以如此高超，全是靠衣（军）装撩呀。<noscript><img src="https://pic3.zhimg.com/6d5354cb3d8307031e09edbfdc6fc882_b.jpg" data-rawwidth="639" data-rawheight="425" class="origin_image zh-lightbox-thumb" width="639" data-original="https://pic3.zhimg.com/6d5354cb3d8307031e09edbfdc6fc882_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="639" data-rawheight="425" class="origin_image zh-lightbox-thumb lazy" width="639" data-original="https://pic3.zhimg.com/6d5354cb3d8307031e09edbfdc6fc882_r.jpg" data-actualsrc="https://pic3.zhimg.com/6d5354cb3d8307031e09edbfdc6fc882_b.jpg"><br></p><noscript><img src="https://pic3.zhimg.com/b21aec233fcd11f78a3cc04c2f84351a_b.jpg" data-rawwidth="520" data-rawheight="379" class="origin_image zh-lightbox-thumb" width="520" data-original="https://pic3.zhimg.com/b21aec233fcd11f78a3cc04c2f84351a_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="520" data-rawheight="379" class="origin_image zh-lightbox-thumb lazy" width="520" data-original="https://pic3.zhimg.com/b21aec233fcd11f78a3cc04c2f84351a_r.jpg" data-actualsrc="https://pic3.zhimg.com/b21aec233fcd11f78a3cc04c2f84351a_b.jpg"><br><br><noscript><img src="https://pic1.zhimg.com/afce70af39e26839a46e9b0acd0422c4_b.jpg" data-rawwidth="520" data-rawheight="769" class="origin_image zh-lightbox-thumb" width="520" data-original="https://pic1.zhimg.com/afce70af39e26839a46e9b0acd0422c4_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="520" data-rawheight="769" class="origin_image zh-lightbox-thumb lazy" width="520" data-original="https://pic1.zhimg.com/afce70af39e26839a46e9b0acd0422c4_r.jpg" data-actualsrc="https://pic1.zhimg.com/afce70af39e26839a46e9b0acd0422c4_b.jpg"><br><noscript><img src="https://pic3.zhimg.com/300370a1de07d9a6ff3b068ce1580ab2_b.jpg" data-rawwidth="640" data-rawheight="360" class="origin_image zh-lightbox-thumb" width="640" data-original="https://pic3.zhimg.com/300370a1de07d9a6ff3b068ce1580ab2_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="640" data-rawheight="360" class="origin_image zh-lightbox-thumb lazy" width="640" data-original="https://pic3.zhimg.com/300370a1de07d9a6ff3b068ce1580ab2_r.jpg" data-actualsrc="https://pic3.zhimg.com/300370a1de07d9a6ff3b068ce1580ab2_b.jpg"><br><p>试问，妹子们看到这样的军装look，少女心能不蓬勃发展么。</p><br><p>今天，范主和范友们聊一聊，那些在时尚界经典不衰，作为常青树活跃在时尚达人们的军装look。</p><br><p><strong>第1部分：服装方面</strong></p><p><strong>☞1.海魂衫</strong><br></p><p>其实就是范友们熟知的条纹衫啦，现在大多数的博主和网红都会大力推荐，穿上海魂衫的柳大尉，简单，干净，充满了夏日气息。<br></p><noscript><img src="https://pic2.zhimg.com/19d55210d8135c3dde44f737006b67e5_b.jpg" data-rawwidth="600" data-rawheight="399" class="origin_image zh-lightbox-thumb" width="600" data-original="https://pic2.zhimg.com/19d55210d8135c3dde44f737006b67e5_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="600" data-rawheight="399" class="origin_image zh-lightbox-thumb lazy" width="600" data-original="https://pic2.zhimg.com/19d55210d8135c3dde44f737006b67e5_r.jpg" data-actualsrc="https://pic2.zhimg.com/19d55210d8135c3dde44f737006b67e5_b.jpg"><br><p>范主的衣柜也有好几件备用的海魂衫，对它是爱不释手。在不知道穿什么的情况下，拿一件海魂衫套身上总是能一解燃眉之急。这种带有淡淡法式风情的条纹衣，最初是19世纪20年代法国海军们在海上穿的，从法国西北方的布列塔尼地区慢慢发展起来。</p><noscript><img src="https://pic1.zhimg.com/77275a4100618258cc8a5c089bc1c780_b.jpg" data-rawwidth="550" data-rawheight="543" class="origin_image zh-lightbox-thumb" width="550" data-original="https://pic1.zhimg.com/77275a4100618258cc8a5c089bc1c780_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="550" data-rawheight="543" class="origin_image zh-lightbox-thumb lazy" width="550" data-original="https://pic1.zhimg.com/77275a4100618258cc8a5c089bc1c780_r.jpg" data-actualsrc="https://pic1.zhimg.com/77275a4100618258cc8a5c089bc1c780_b.jpg"><br><br><p>早期一件真正的海魂衫必须具备三个条件才能被法国官方称为海魂衫：</p><p><strong>1.领子下，必须有21条白纹（每条白纹都代表着拿破仑领导的海军对外作战的胜利）。</strong><br></p><p><strong>2.袖子上，必须有15条白纹。</strong><br></p><p><strong>3.手工羊毛制成。（不过现在是棉质的了）</strong></p><br><p>既然海魂衫是给水手们穿的，为什么它会和时尚圈扯上关系，且在时尚圈占有一席之位呢？</p><noscript><img src="https://pic2.zhimg.com/d745d01276a4876e4230680e2def4d09_b.jpg" data-rawwidth="640" data-rawheight="971" class="origin_image zh-lightbox-thumb" width="640" data-original="https://pic2.zhimg.com/d745d01276a4876e4230680e2def4d09_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="640" data-rawheight="971" class="origin_image zh-lightbox-thumb lazy" width="640" data-original="https://pic2.zhimg.com/d745d01276a4876e4230680e2def4d09_r.jpg" data-actualsrc="https://pic2.zhimg.com/d745d01276a4876e4230680e2def4d09_b.jpg"><br><br><p>这要归功于法国女作家科莱特(Colette)和可可·香奈尔在名人界的不经意推广了，一次，科莱特去参加巴黎的名人趴，就是以一件条纹衫出席晚会趴。</p><noscript><img src="https://pic1.zhimg.com/7f36a969594169272af41f4f03728b9c_b.jpg" data-rawwidth="634" data-rawheight="803" class="origin_image zh-lightbox-thumb" width="634" data-original="https://pic1.zhimg.com/7f36a969594169272af41f4f03728b9c_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="634" data-rawheight="803" class="origin_image zh-lightbox-thumb lazy" width="634" data-original="https://pic1.zhimg.com/7f36a969594169272af41f4f03728b9c_r.jpg" data-actualsrc="https://pic1.zhimg.com/7f36a969594169272af41f4f03728b9c_b.jpg"><br><p>可可·香奈尔本身就是裁缝出身，设计自己品牌衣服时，就将海魂衫融入进去，制成商品出售。<noscript><img src="https://pic3.zhimg.com/7f013cdfa32d3771b12cf2ead3e0c236_b.jpg" data-rawwidth="551" data-rawheight="605" class="origin_image zh-lightbox-thumb" width="551" data-original="https://pic3.zhimg.com/7f013cdfa32d3771b12cf2ead3e0c236_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="551" data-rawheight="605" class="origin_image zh-lightbox-thumb lazy" width="551" data-original="https://pic3.zhimg.com/7f013cdfa32d3771b12cf2ead3e0c236_r.jpg" data-actualsrc="https://pic3.zhimg.com/7f013cdfa32d3771b12cf2ead3e0c236_b.jpg"><br></p><br><p>慢慢的，海魂衫就开始走向世界，并且一直引领着夏日度假风潮，现在不少大牌也将海魂衫放入自己的创作中，每年的新款都会有海魂衫的影子出现。以下皆为男士款。</p><br><p><strong><strong>▶ Saint Laurent</strong></strong></p><noscript><img src="https://pic4.zhimg.com/9883ce36c642a2b917bea595988d1dff_b.jpg" data-rawwidth="402" data-rawheight="598" class="content_image" width="402"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="402" data-rawheight="598" class="content_image lazy" width="402" data-actualsrc="https://pic4.zhimg.com/9883ce36c642a2b917bea595988d1dff_b.jpg"><br><br><p><strong>▶ Sandro</strong></p><noscript><img src="https://pic1.zhimg.com/ae93b1bf5b87fbc481895d43993917e0_b.jpg" data-rawwidth="401" data-rawheight="600" class="content_image" width="401"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="401" data-rawheight="600" class="content_image lazy" width="401" data-actualsrc="https://pic1.zhimg.com/ae93b1bf5b87fbc481895d43993917e0_b.jpg"><br><br><p><strong>▶</strong><strong>Gant Rugger</strong></p><br><noscript><img src="https://pic3.zhimg.com/54b454c56b583eb214eb4573df629f5a_b.jpg" data-rawwidth="569" data-rawheight="450" class="origin_image zh-lightbox-thumb" width="569" data-original="https://pic3.zhimg.com/54b454c56b583eb214eb4573df629f5a_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="569" data-rawheight="450" class="origin_image zh-lightbox-thumb lazy" width="569" data-original="https://pic3.zhimg.com/54b454c56b583eb214eb4573df629f5a_r.jpg" data-actualsrc="https://pic3.zhimg.com/54b454c56b583eb214eb4573df629f5a_b.jpg"><br><p><strong><strong>▶</strong><strong>H&amp;M </strong></strong></p><noscript><img src="https://pic1.zhimg.com/0de423ef34f384911575bc7927979a40_b.jpg" data-rawwidth="640" data-rawheight="430" class="origin_image zh-lightbox-thumb" width="640" data-original="https://pic1.zhimg.com/0de423ef34f384911575bc7927979a40_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="640" data-rawheight="430" class="origin_image zh-lightbox-thumb lazy" width="640" data-original="https://pic1.zhimg.com/0de423ef34f384911575bc7927979a40_r.jpg" data-actualsrc="https://pic1.zhimg.com/0de423ef34f384911575bc7927979a40_b.jpg"><br><p><strong>☞2.飞行夹克</strong></p><p>飞行夹克，虽然没有在剧中出现，但这款源于军装的look也是很有看头的，在男生不知道要穿什么外套，飞行员夹克就是很好的选择。英文叫Bomber jacket或者Flight jacket。最初是米国设计给空军战士们御寒保暖用的。</p><noscript><img src="https://pic1.zhimg.com/9d5ec4bc11de435458394a5d7020c764_b.jpg" data-rawwidth="520" data-rawheight="316" class="origin_image zh-lightbox-thumb" width="520" data-original="https://pic1.zhimg.com/9d5ec4bc11de435458394a5d7020c764_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="520" data-rawheight="316" class="origin_image zh-lightbox-thumb lazy" width="520" data-original="https://pic1.zhimg.com/9d5ec4bc11de435458394a5d7020c764_r.jpg" data-actualsrc="https://pic1.zhimg.com/9d5ec4bc11de435458394a5d7020c764_b.jpg"><br><p>一战时期的飞行夹克还只是一个萌芽阶段，发展到二战之后，飞行夹克和现在各个品牌推出的夹克样子大体一致。</p><noscript><img src="https://pic4.zhimg.com/5dd221cc75b36df1fccbe68a4281370b_b.jpg" data-rawwidth="560" data-rawheight="711" class="origin_image zh-lightbox-thumb" width="560" data-original="https://pic4.zhimg.com/5dd221cc75b36df1fccbe68a4281370b_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="560" data-rawheight="711" class="origin_image zh-lightbox-thumb lazy" width="560" data-original="https://pic4.zhimg.com/5dd221cc75b36df1fccbe68a4281370b_r.jpg" data-actualsrc="https://pic4.zhimg.com/5dd221cc75b36df1fccbe68a4281370b_b.jpg"><br><br><p>飞行夹克有几点特点：</p><p><strong>1.轻薄（</strong>考虑到作战期间，战士们穿着能够活动自如<strong>）</strong></p><p><strong>2.袖扣和下摆紧贴身体（</strong>防止风从里灌入<strong>）</strong></p><p><strong>3.衣服要带领（</strong>保暖，总不能裹着一条围巾打仗吧<strong>）。</strong></p><noscript><img src="https://pic2.zhimg.com/84d615b24103eaeac717f1e56c3317f1_b.jpg" data-rawwidth="640" data-rawheight="689" class="origin_image zh-lightbox-thumb" width="640" data-original="https://pic2.zhimg.com/84d615b24103eaeac717f1e56c3317f1_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="640" data-rawheight="689" class="origin_image zh-lightbox-thumb lazy" width="640" data-original="https://pic2.zhimg.com/84d615b24103eaeac717f1e56c3317f1_r.jpg" data-actualsrc="https://pic2.zhimg.com/84d615b24103eaeac717f1e56c3317f1_b.jpg"><br><br><p>如今，被大众熟悉的是A2，B3，MA-1、B-15C等夹克。</p><noscript><img src="https://pic1.zhimg.com/b6535d9382f033c8862bfff55cf46168_b.jpg" data-rawwidth="590" data-rawheight="331" class="origin_image zh-lightbox-thumb" width="590" data-original="https://pic1.zhimg.com/b6535d9382f033c8862bfff55cf46168_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="590" data-rawheight="331" class="origin_image zh-lightbox-thumb lazy" width="590" data-original="https://pic1.zhimg.com/b6535d9382f033c8862bfff55cf46168_r.jpg" data-actualsrc="https://pic1.zhimg.com/b6535d9382f033c8862bfff55cf46168_b.jpg"><br><p><strong>电影《珍珠港》穿的是A2</strong></p><br><p>奥巴马慰问美国大兵时，穿的是飞行夹克A-2。这款大衣一般都是采用棕色或者深色的真皮制成，主要是防风，保暖效果一般。</p><noscript><img src="https://pic1.zhimg.com/862d552065bbf3a3a075587dafd6ac24_b.jpg" data-rawwidth="640" data-rawheight="366" class="origin_image zh-lightbox-thumb" width="640" data-original="https://pic1.zhimg.com/862d552065bbf3a3a075587dafd6ac24_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="640" data-rawheight="366" class="origin_image zh-lightbox-thumb lazy" width="640" data-original="https://pic1.zhimg.com/862d552065bbf3a3a075587dafd6ac24_r.jpg" data-actualsrc="https://pic1.zhimg.com/862d552065bbf3a3a075587dafd6ac24_b.jpg"><br><br><p>最经典的是MA-1，侃爷（Kanye West）身上这件绿色的就是MA-1，因为它轻薄，材质大部分都是尼龙面料。用他搭配T恤或者外搭卫衣，都是生活中休闲的穿搭方式。<br></p><noscript><img src="https://pic4.zhimg.com/820efde4a25bfa8a65c19dee81a1eabf_b.jpg" data-rawwidth="640" data-rawheight="640" class="origin_image zh-lightbox-thumb" width="640" data-original="https://pic4.zhimg.com/820efde4a25bfa8a65c19dee81a1eabf_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="640" data-rawheight="640" class="origin_image zh-lightbox-thumb lazy" width="640" data-original="https://pic4.zhimg.com/820efde4a25bfa8a65c19dee81a1eabf_r.jpg" data-actualsrc="https://pic4.zhimg.com/820efde4a25bfa8a65c19dee81a1eabf_b.jpg"><br><p>不少街拍达人也会选择用MA-1来演绎秋冬look，的确cool，和侃爷不同的是，他们MA-1是针织的衣领。飞行员夹克MA-1和棒球衫比较像，唯一不同的是棒球衫是用纽扣，飞行员夹克则是用拉链一拉而上。</p><noscript><img src="https://pic2.zhimg.com/19f23017965e4a8eb57e4c047ad0cdf1_b.jpg" data-rawwidth="500" data-rawheight="500" class="origin_image zh-lightbox-thumb" width="500" data-original="https://pic2.zhimg.com/19f23017965e4a8eb57e4c047ad0cdf1_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="500" data-rawheight="500" class="origin_image zh-lightbox-thumb lazy" width="500" data-original="https://pic2.zhimg.com/19f23017965e4a8eb57e4c047ad0cdf1_r.jpg" data-actualsrc="https://pic2.zhimg.com/19f23017965e4a8eb57e4c047ad0cdf1_b.jpg"><br><noscript><img src="https://pic3.zhimg.com/37ad3133c356a944f815c5574c6a3cce_b.jpg" data-rawwidth="525" data-rawheight="400" class="origin_image zh-lightbox-thumb" width="525" data-original="https://pic3.zhimg.com/37ad3133c356a944f815c5574c6a3cce_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="525" data-rawheight="400" class="origin_image zh-lightbox-thumb lazy" width="525" data-original="https://pic3.zhimg.com/37ad3133c356a944f815c5574c6a3cce_r.jpg" data-actualsrc="https://pic3.zhimg.com/37ad3133c356a944f815c5574c6a3cce_b.jpg"><br><p>在这里还要说下，如果男性范友选择飞行员夹克MA-1，肚子稍微有点大的，一定不要把拉链拉上，<br></p><noscript><img src="https://pic2.zhimg.com/94bce3301bc0a84c1a3e2953ad776305_b.jpg" data-rawwidth="550" data-rawheight="700" class="origin_image zh-lightbox-thumb" width="550" data-original="https://pic2.zhimg.com/94bce3301bc0a84c1a3e2953ad776305_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="550" data-rawheight="700" class="origin_image zh-lightbox-thumb lazy" width="550" data-original="https://pic2.zhimg.com/94bce3301bc0a84c1a3e2953ad776305_r.jpg" data-actualsrc="https://pic2.zhimg.com/94bce3301bc0a84c1a3e2953ad776305_b.jpg"><br><p>拉上之后会拉低身材的弧度美，就比如美国演员Bradley Cooper，拉上之后，肚子咋感觉那么鼓鼓的呢！</p><noscript><img src="https://pic4.zhimg.com/766e5b54ba3011d45c45715448e1a47b_b.jpg" data-rawwidth="435" data-rawheight="580" class="origin_image zh-lightbox-thumb" width="435" data-original="https://pic4.zhimg.com/766e5b54ba3011d45c45715448e1a47b_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="435" data-rawheight="580" class="origin_image zh-lightbox-thumb lazy" width="435" data-original="https://pic4.zhimg.com/766e5b54ba3011d45c45715448e1a47b_r.jpg" data-actualsrc="https://pic4.zhimg.com/766e5b54ba3011d45c45715448e1a47b_b.jpg"><br><p>但身形消瘦，风大还是可以拉上的（<strong>瘦子穿什么都是美的X﹏X</strong>）</p><noscript><img src="https://pic1.zhimg.com/33014c2cdb1e3c73952409f2752de034_b.jpg" data-rawwidth="380" data-rawheight="570" class="content_image" width="380"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="380" data-rawheight="570" class="content_image lazy" width="380" data-actualsrc="https://pic1.zhimg.com/33014c2cdb1e3c73952409f2752de034_b.jpg"><br><br><p>B-3和其他衣服对比，材质上就显得很臃肿了。但是它真的很暖和啊，嘿嘿，价格也是让人吃土。</p><noscript><img src="https://pic1.zhimg.com/79e7546a8b2a43fc967f5de34bba6a24_b.jpg" data-rawwidth="495" data-rawheight="745" class="origin_image zh-lightbox-thumb" width="495" data-original="https://pic1.zhimg.com/79e7546a8b2a43fc967f5de34bba6a24_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="495" data-rawheight="745" class="origin_image zh-lightbox-thumb lazy" width="495" data-original="https://pic1.zhimg.com/79e7546a8b2a43fc967f5de34bba6a24_r.jpg" data-actualsrc="https://pic1.zhimg.com/79e7546a8b2a43fc967f5de34bba6a24_b.jpg"><br><br><p>二战期间，为了让空军战士在作战时，能够抵挡寒冷的高空环境，将飞行夹克的材质，用保暖的羊羔毛代替，这个创意还是借鉴了尼泊尔的一个少数民族—夏尔巴人。他们长期生活在高寒地带，穿着自制的一种皮大衣，皮大衣的里面是一层厚厚的羊羔毛，这种衣服穿上后对于御寒保暖十分有用。B-3也是巧妙的将这一理念融入设计中。</p><noscript><img src="https://pic4.zhimg.com/536d17f6b5bc978e6930aa75e033bfb3_b.jpg" data-rawwidth="620" data-rawheight="437" class="origin_image zh-lightbox-thumb" width="620" data-original="https://pic4.zhimg.com/536d17f6b5bc978e6930aa75e033bfb3_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="620" data-rawheight="437" class="origin_image zh-lightbox-thumb lazy" width="620" data-original="https://pic4.zhimg.com/536d17f6b5bc978e6930aa75e033bfb3_r.jpg" data-actualsrc="https://pic4.zhimg.com/536d17f6b5bc978e6930aa75e033bfb3_b.jpg"><br><br><p>巴顿将军不论是电影中还是现实拍摄到的照片中，穿B-3飞行夹克还是很常见的。</p><br><noscript><img src="https://pic3.zhimg.com/a1dc1cae91c7ab526dad31b6cd1895c2_b.jpg" data-rawwidth="474" data-rawheight="599" class="origin_image zh-lightbox-thumb" width="474" data-original="https://pic3.zhimg.com/a1dc1cae91c7ab526dad31b6cd1895c2_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="474" data-rawheight="599" class="origin_image zh-lightbox-thumb lazy" width="474" data-original="https://pic3.zhimg.com/a1dc1cae91c7ab526dad31b6cd1895c2_r.jpg" data-actualsrc="https://pic3.zhimg.com/a1dc1cae91c7ab526dad31b6cd1895c2_b.jpg"><br><p>谢霆锋对B-3也有不一样的情节，曾经媒体说他9年不换衣，还穿着当年的B-3</p><noscript><img src="https://pic3.zhimg.com/151d9b4b6a4fcfb8b68dcafdc1f44b06_b.jpg" data-rawwidth="475" data-rawheight="600" class="origin_image zh-lightbox-thumb" width="475" data-original="https://pic3.zhimg.com/151d9b4b6a4fcfb8b68dcafdc1f44b06_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="475" data-rawheight="600" class="origin_image zh-lightbox-thumb lazy" width="475" data-original="https://pic3.zhimg.com/151d9b4b6a4fcfb8b68dcafdc1f44b06_r.jpg" data-actualsrc="https://pic3.zhimg.com/151d9b4b6a4fcfb8b68dcafdc1f44b06_b.jpg"><br><br><br><p>飞行夹克在各大品牌中，也是常见的角色。<br></p><br><p><strong>▶Dior homme</strong></p><p>在2012年Dior homme秋冬男装，就以不一样的剪裁风格打造独特的军装，用以羊羔绒的衣领搭配皮质的上衣</p><noscript><img src="https://pic4.zhimg.com/975837dcc8305ccdadf84868257cf9db_b.jpg" data-rawwidth="400" data-rawheight="598" class="content_image" width="400"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="400" data-rawheight="598" class="content_image lazy" width="400" data-actualsrc="https://pic4.zhimg.com/975837dcc8305ccdadf84868257cf9db_b.jpg"><br><noscript><img src="https://pic4.zhimg.com/3583b1e947494a72501280ad8e91c3f3_b.jpg" data-rawwidth="402" data-rawheight="602" class="content_image" width="402"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="402" data-rawheight="602" class="content_image lazy" width="402" data-actualsrc="https://pic4.zhimg.com/3583b1e947494a72501280ad8e91c3f3_b.jpg"><br><noscript><img src="https://pic2.zhimg.com/4b54a4202a6c21a37eaf92312b0b7e41_b.jpg" data-rawwidth="407" data-rawheight="604" class="content_image" width="407"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="407" data-rawheight="604" class="content_image lazy" width="407" data-actualsrc="https://pic2.zhimg.com/4b54a4202a6c21a37eaf92312b0b7e41_b.jpg"><br><br><p><strong>▶Neil Barrett</strong></p><p>Neil Barrett在2012秋冬男装采用拼接版的飞行夹克，上身和袖扣都是紧贴身体，很好的抵御大风的入侵。<br></p><noscript><img src="https://pic3.zhimg.com/097e28e013d578aa5d1be7023bdd4012_b.jpg" data-rawwidth="399" data-rawheight="598" class="content_image" width="399"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="399" data-rawheight="598" class="content_image lazy" width="399" data-actualsrc="https://pic3.zhimg.com/097e28e013d578aa5d1be7023bdd4012_b.jpg"><br><p><strong>▶Diesel Black Gold</strong></p><p>觉得色彩太单调了，2012秋冬男装Diesel Black Gold出的这款针织系列给你不一样的拼接色。</p><noscript><img src="https://pic2.zhimg.com/653b700446c9a6c3de044f630e0fd879_b.jpg" data-rawwidth="401" data-rawheight="599" class="content_image" width="401"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="401" data-rawheight="599" class="content_image lazy" width="401" data-actualsrc="https://pic2.zhimg.com/653b700446c9a6c3de044f630e0fd879_b.jpg"><br><br><p><strong>第2部分：配饰方面</strong></p><br><p>宋仲基在剧中饰演的柳大尉，和女主碰面时戴的那幅眼镜，是有名的蛤蟆镜—Ray-Ban。不知道细心的范友有没有注意，柳大尉和其他几个队员一起走，就他戴了墨镜，为啥？答案：凸显自己更帅。</p><noscript><img src="https://pic1.zhimg.com/fb166d5c78e0d01fd889b3ac797cfbec_b.jpg" data-rawwidth="600" data-rawheight="399" class="origin_image zh-lightbox-thumb" width="600" data-original="https://pic1.zhimg.com/fb166d5c78e0d01fd889b3ac797cfbec_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="600" data-rawheight="399" class="origin_image zh-lightbox-thumb lazy" width="600" data-original="https://pic1.zhimg.com/fb166d5c78e0d01fd889b3ac797cfbec_r.jpg" data-actualsrc="https://pic1.zhimg.com/fb166d5c78e0d01fd889b3ac797cfbec_b.jpg"><br><br><p><strong>☞1.Ray-Ban</strong></p><p>Ray-Ban于1930年创立的，（这部剧热播时，范友的好朋友就说，以前觉得Ray-Ban不好看，现在好想去剁手买一副戴一戴，而且一定是宋仲基同款。）</p><noscript><img src="https://pic2.zhimg.com/c9f65bc95981bf30058854fdcecfb2d1_b.jpg" data-rawwidth="540" data-rawheight="303" class="origin_image zh-lightbox-thumb" width="540" data-original="https://pic2.zhimg.com/c9f65bc95981bf30058854fdcecfb2d1_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="540" data-rawheight="303" class="origin_image zh-lightbox-thumb lazy" width="540" data-original="https://pic2.zhimg.com/c9f65bc95981bf30058854fdcecfb2d1_r.jpg" data-actualsrc="https://pic2.zhimg.com/c9f65bc95981bf30058854fdcecfb2d1_b.jpg"><br><br><p>虽然范主觉得剁手要理性，但是Ray-Ban从专业性来说，还是比较值得入手的。最早，一位美国的空军向博士伦眼镜公司反映，希望能够开发出一款能够保护在飞行过程中遇到太阳光强烈照射的眼睛的眼镜。后来，博士伦公司在1930年就研发出了雷朋眼镜。</p><br><p>雷朋眼镜自产生之后，几十年过去了，在好莱坞圈子中，依然广受追捧。美国演员兼歌手主持人的Justin Timberlake就戴着雷朋在公众亮相。<br></p><noscript><img src="https://pic4.zhimg.com/8df5387489405f56283066dffceab9a7_b.jpg" data-rawwidth="327" data-rawheight="415" class="content_image" width="327"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="327" data-rawheight="415" class="content_image lazy" width="327" data-actualsrc="https://pic4.zhimg.com/8df5387489405f56283066dffceab9a7_b.jpg"><br><p>《暮光之城》的男主角</p><noscript><img src="https://pic4.zhimg.com/e3bdfcd320704f27098d3b2ef1f2ef33_b.jpg" data-rawwidth="550" data-rawheight="458" class="origin_image zh-lightbox-thumb" width="550" data-original="https://pic4.zhimg.com/e3bdfcd320704f27098d3b2ef1f2ef33_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="550" data-rawheight="458" class="origin_image zh-lightbox-thumb lazy" width="550" data-original="https://pic4.zhimg.com/e3bdfcd320704f27098d3b2ef1f2ef33_r.jpg" data-actualsrc="https://pic4.zhimg.com/e3bdfcd320704f27098d3b2ef1f2ef33_b.jpg"><br><p>阿汤哥</p><noscript><img src="https://pic4.zhimg.com/c963a3b481ed25de5f8303f8d974299f_b.jpg" data-rawwidth="640" data-rawheight="964" class="origin_image zh-lightbox-thumb" width="640" data-original="https://pic4.zhimg.com/c963a3b481ed25de5f8303f8d974299f_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="640" data-rawheight="964" class="origin_image zh-lightbox-thumb lazy" width="640" data-original="https://pic4.zhimg.com/c963a3b481ed25de5f8303f8d974299f_r.jpg" data-actualsrc="https://pic4.zhimg.com/c963a3b481ed25de5f8303f8d974299f_b.jpg"><br><p>朱莉的老公布拉德皮特</p><noscript><img src="https://pic4.zhimg.com/8b9cf5793a641e75f1dc40e6e58993e3_b.jpg" data-rawwidth="291" data-rawheight="400" class="content_image" width="291"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="291" data-rawheight="400" class="content_image lazy" width="291" data-actualsrc="https://pic4.zhimg.com/8b9cf5793a641e75f1dc40e6e58993e3_b.jpg"><br><p>加勒比海盗船长，约翰尼·德普<br></p><noscript><img src="https://pic4.zhimg.com/8eb332b28f26ac4d7055341c25b5eb03_b.jpg" data-rawwidth="495" data-rawheight="482" class="origin_image zh-lightbox-thumb" width="495" data-original="https://pic4.zhimg.com/8eb332b28f26ac4d7055341c25b5eb03_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="495" data-rawheight="482" class="origin_image zh-lightbox-thumb lazy" width="495" data-original="https://pic4.zhimg.com/8eb332b28f26ac4d7055341c25b5eb03_r.jpg" data-actualsrc="https://pic4.zhimg.com/8eb332b28f26ac4d7055341c25b5eb03_b.jpg"><br><p>咱们的老朋友小扎等鼻梁上都爱驾着雷朋，透露出一种不一样的自信。</p><noscript><img src="https://pic4.zhimg.com/e0742ccef444fd05f85550e2a2d27edf_b.jpg" data-rawwidth="640" data-rawheight="424" class="origin_image zh-lightbox-thumb" width="640" data-original="https://pic4.zhimg.com/e0742ccef444fd05f85550e2a2d27edf_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="640" data-rawheight="424" class="origin_image zh-lightbox-thumb lazy" width="640" data-original="https://pic4.zhimg.com/e0742ccef444fd05f85550e2a2d27edf_r.jpg" data-actualsrc="https://pic4.zhimg.com/e0742ccef444fd05f85550e2a2d27edf_b.jpg"><br><p><strong>☞2.贝雷帽</strong></p><p>在剧中频频出现的还有柳大尉的贝雷帽。这种无檐软质制式军帽，是国家特种部队、特别行动队和空降队的队员们戴的。</p><noscript><img src="https://pic1.zhimg.com/8bb61cd773b8e6cbdc6c2a98804a0798_b.jpg" data-rawwidth="495" data-rawheight="542" class="origin_image zh-lightbox-thumb" width="495" data-original="https://pic1.zhimg.com/8bb61cd773b8e6cbdc6c2a98804a0798_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="495" data-rawheight="542" class="origin_image zh-lightbox-thumb lazy" width="495" data-original="https://pic1.zhimg.com/8bb61cd773b8e6cbdc6c2a98804a0798_r.jpg" data-actualsrc="https://pic1.zhimg.com/8bb61cd773b8e6cbdc6c2a98804a0798_b.jpg"><br><p>最早是英国的军队开始戴的。它的颜色有6种，分别是栗色、绿色、黑色、红色、黄色、蓝色。颜色不同，所代表的意义也不一样。</p><noscript><img src="https://pic1.zhimg.com/28c748273ac6f1b5ff1549278e2612d0_b.jpg" data-rawwidth="620" data-rawheight="413" class="origin_image zh-lightbox-thumb" width="620" data-original="https://pic1.zhimg.com/28c748273ac6f1b5ff1549278e2612d0_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="620" data-rawheight="413" class="origin_image zh-lightbox-thumb lazy" width="620" data-original="https://pic1.zhimg.com/28c748273ac6f1b5ff1549278e2612d0_r.jpg" data-actualsrc="https://pic1.zhimg.com/28c748273ac6f1b5ff1549278e2612d0_b.jpg"><br><br><p>但贝雷帽和时尚拉上关系，是一个叫Jean Borotra的网球选手，1920年他在一次比赛中，带着自己家乡的贝雷帽和对手PK，因为戴着帽子运动，帽子会一个不小心掉下来，Jean Borotra就会自己停下比赛，中途调整下帽子的位置。慢慢的，就流传在欧洲贵族中了，</p><noscript><img src="https://pic4.zhimg.com/b5091274d1f49198450c0eef1ae220b3_b.jpg" data-rawwidth="640" data-rawheight="480" class="origin_image zh-lightbox-thumb" width="640" data-original="https://pic4.zhimg.com/b5091274d1f49198450c0eef1ae220b3_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="640" data-rawheight="480" class="origin_image zh-lightbox-thumb lazy" width="640" data-original="https://pic4.zhimg.com/b5091274d1f49198450c0eef1ae220b3_r.jpg" data-actualsrc="https://pic4.zhimg.com/b5091274d1f49198450c0eef1ae220b3_b.jpg"><br><p>其中，还有一些文豪艺术家，在他们的画像中，也有戴着贝雷帽的影子。<br></p><noscript><img src="https://pic4.zhimg.com/ad65ba8f61c8f5d9460e304397d4f167_b.jpg" data-rawwidth="640" data-rawheight="480" class="origin_image zh-lightbox-thumb" width="640" data-original="https://pic4.zhimg.com/ad65ba8f61c8f5d9460e304397d4f167_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="640" data-rawheight="480" class="origin_image zh-lightbox-thumb lazy" width="640" data-original="https://pic4.zhimg.com/ad65ba8f61c8f5d9460e304397d4f167_r.jpg" data-actualsrc="https://pic4.zhimg.com/ad65ba8f61c8f5d9460e304397d4f167_b.jpg"><br><p>杰森斯坦森戴着贝雷帽，拿着枪的他散发着一种不一样男子气概。<noscript><img src="https://pic4.zhimg.com/703fa408857c8ac47f1407c48d5dff8f_b.jpg" data-rawwidth="640" data-rawheight="427" class="origin_image zh-lightbox-thumb" width="640" data-original="https://pic4.zhimg.com/703fa408857c8ac47f1407c48d5dff8f_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="640" data-rawheight="427" class="origin_image zh-lightbox-thumb lazy" width="640" data-original="https://pic4.zhimg.com/703fa408857c8ac47f1407c48d5dff8f_r.jpg" data-actualsrc="https://pic4.zhimg.com/703fa408857c8ac47f1407c48d5dff8f_b.jpg"><br></p><p>不管是哪一类人，艺术家，网球运动员，演员还有以下这些大牌，都喜欢用不同的形式，来展现对贝雷帽的喜爱。<br></p><br><p><strong>▶</strong><strong>Emporio Armani</strong></p><noscript><img src="https://pic2.zhimg.com/a6967cdee095966df7217fe87dc26021_b.jpg" data-rawwidth="640" data-rawheight="480" class="origin_image zh-lightbox-thumb" width="640" data-original="https://pic2.zhimg.com/a6967cdee095966df7217fe87dc26021_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="640" data-rawheight="480" class="origin_image zh-lightbox-thumb lazy" width="640" data-original="https://pic2.zhimg.com/a6967cdee095966df7217fe87dc26021_r.jpg" data-actualsrc="https://pic2.zhimg.com/a6967cdee095966df7217fe87dc26021_b.jpg"><br><p><strong>▶Saint Laurent</strong></p><noscript><img src="https://pic2.zhimg.com/ab22f98616a7bfcadfa1f7c8b2d98f71_b.jpg" data-rawwidth="640" data-rawheight="480" class="origin_image zh-lightbox-thumb" width="640" data-original="https://pic2.zhimg.com/ab22f98616a7bfcadfa1f7c8b2d98f71_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="640" data-rawheight="480" class="origin_image zh-lightbox-thumb lazy" width="640" data-original="https://pic2.zhimg.com/ab22f98616a7bfcadfa1f7c8b2d98f71_r.jpg" data-actualsrc="https://pic2.zhimg.com/ab22f98616a7bfcadfa1f7c8b2d98f71_b.jpg"><br><p><strong><strong><strong>▶</strong></strong>Gucci</strong></p><noscript><img src="https://pic2.zhimg.com/bf66c6191aded13a4a4328553da98ba1_b.jpg" data-rawwidth="640" data-rawheight="480" class="origin_image zh-lightbox-thumb" width="640" data-original="https://pic2.zhimg.com/bf66c6191aded13a4a4328553da98ba1_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="640" data-rawheight="480" class="origin_image zh-lightbox-thumb lazy" width="640" data-original="https://pic2.zhimg.com/bf66c6191aded13a4a4328553da98ba1_r.jpg" data-actualsrc="https://pic2.zhimg.com/bf66c6191aded13a4a4328553da98ba1_b.jpg"><br><br><p><strong>第3部分：军装LOOK为什么广受追捧</strong></p><p>《太阳的后裔》自从播出后就刷遍各大媒体，开启霸屏模式，不仅把之前韩剧最火的《星你》挤爆，更是抢走了《奶酪陷阱》的热度。每次看到柳大尉穿着军装制服，在戏中精彩的表现，戏外的妹子们就会大呼：穿军装的男人超帅啊，我要睡他~~~<noscript><img src="https://pic4.zhimg.com/fe0121ec974842e357379006fe82076b_b.jpg" data-rawwidth="600" data-rawheight="337" class="origin_image zh-lightbox-thumb" width="600" data-original="https://pic4.zhimg.com/fe0121ec974842e357379006fe82076b_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="600" data-rawheight="337" class="origin_image zh-lightbox-thumb lazy" width="600" data-original="https://pic4.zhimg.com/fe0121ec974842e357379006fe82076b_r.jpg" data-actualsrc="https://pic4.zhimg.com/fe0121ec974842e357379006fe82076b_b.jpg"><br></p><br><p>看到如此鸡冻的妹子们，范主就想到了国外曾经有一个调查</p><blockquote><p>英国某歌剧曾经做过一次调查，3000名的成人中，感情上是第三者的女性，有25%是不会拒绝穿制服的男人。</p></blockquote><br><p>军人的制服，本身就有一种不一样的诱惑。穿上它的男生，是身份转变的象征，体现了男性本身的雄性魅力。从生理的角度来说，穿制服的男性会更加触动女性对异性的性冲动。</p><noscript><img src="https://pic3.zhimg.com/5dd102020623b2625769a0588ea4b98a_b.jpg" data-rawwidth="600" data-rawheight="337" class="origin_image zh-lightbox-thumb" width="600" data-original="https://pic3.zhimg.com/5dd102020623b2625769a0588ea4b98a_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="600" data-rawheight="337" class="origin_image zh-lightbox-thumb lazy" width="600" data-original="https://pic3.zhimg.com/5dd102020623b2625769a0588ea4b98a_r.jpg" data-actualsrc="https://pic3.zhimg.com/5dd102020623b2625769a0588ea4b98a_b.jpg"><br><br><p>在网上充斥着我要睡宋仲基，以及这样的表情包，就不难想象，穿制服的男人到底多有魅力了。</p><noscript><img src="https://pic3.zhimg.com/4c66aafc265bc54bf1be6774cec811fa_b.jpg" data-rawwidth="440" data-rawheight="357" class="origin_image zh-lightbox-thumb" width="440" data-original="https://pic3.zhimg.com/4c66aafc265bc54bf1be6774cec811fa_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="440" data-rawheight="357" class="origin_image zh-lightbox-thumb lazy" width="440" data-original="https://pic3.zhimg.com/4c66aafc265bc54bf1be6774cec811fa_r.jpg" data-actualsrc="https://pic3.zhimg.com/4c66aafc265bc54bf1be6774cec811fa_b.jpg"><br><p>毕竟，很少有女生能够抵挡得住穿制服的颜，如年轻时的马龙·白兰度，</p><noscript><img src="https://pic3.zhimg.com/bc7cfd9d6e7d13ecf4cfb120bf36360a_b.jpg" data-rawwidth="445" data-rawheight="524" class="origin_image zh-lightbox-thumb" width="445" data-original="https://pic3.zhimg.com/bc7cfd9d6e7d13ecf4cfb120bf36360a_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="445" data-rawheight="524" class="origin_image zh-lightbox-thumb lazy" width="445" data-original="https://pic3.zhimg.com/bc7cfd9d6e7d13ecf4cfb120bf36360a_r.jpg" data-actualsrc="https://pic3.zhimg.com/bc7cfd9d6e7d13ecf4cfb120bf36360a_b.jpg"><br><noscript><img src="https://pic1.zhimg.com/3477fafd4be474bcb6b40613a85d9be0_b.jpg" data-rawwidth="640" data-rawheight="427" class="origin_image zh-lightbox-thumb" width="640" data-original="https://pic1.zhimg.com/3477fafd4be474bcb6b40613a85d9be0_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="640" data-rawheight="427" class="origin_image zh-lightbox-thumb lazy" width="640" data-original="https://pic1.zhimg.com/3477fafd4be474bcb6b40613a85d9be0_r.jpg" data-actualsrc="https://pic1.zhimg.com/3477fafd4be474bcb6b40613a85d9be0_b.jpg"><br><br><p>《美少年之恋》的吴彦祖</p><noscript><img src="https://pic3.zhimg.com/a97137826304a87284298498813fd002_b.jpg" data-rawwidth="398" data-rawheight="459" class="content_image" width="398"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="398" data-rawheight="459" class="content_image lazy" width="398" data-actualsrc="https://pic3.zhimg.com/a97137826304a87284298498813fd002_b.jpg"><br><p>蓝后范主联想到：应该有不少男性范友也喜欢霓虹国穿制服的妹子吧！</p><noscript><img src="https://pic4.zhimg.com/30bb4ca19f82db8ac00535769673346f_b.jpg" data-rawwidth="640" data-rawheight="430" class="origin_image zh-lightbox-thumb" width="640" data-original="https://pic4.zhimg.com/30bb4ca19f82db8ac00535769673346f_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="640" data-rawheight="430" class="origin_image zh-lightbox-thumb lazy" width="640" data-original="https://pic4.zhimg.com/30bb4ca19f82db8ac00535769673346f_r.jpg" data-actualsrc="https://pic4.zhimg.com/30bb4ca19f82db8ac00535769673346f_b.jpg"><br><br><p>但如果是这样的制服，还有少女爱，你说出来，范主一定炒鸡佩服你呢！！</p><noscript><img src="https://pic4.zhimg.com/0aa172a858967d1cde18c2e47611ec37_b.jpg" data-rawwidth="640" data-rawheight="362" class="origin_image zh-lightbox-thumb" width="640" data-original="https://pic4.zhimg.com/0aa172a858967d1cde18c2e47611ec37_r.jpg"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="640" data-rawheight="362" class="origin_image zh-lightbox-thumb lazy" width="640" data-original="https://pic4.zhimg.com/0aa172a858967d1cde18c2e47611ec37_r.jpg" data-actualsrc="https://pic4.zhimg.com/0aa172a858967d1cde18c2e47611ec37_b.jpg"><br><p><b>商务范 | bfaner</b><br></p><p>微信第一风尚自媒体。商务金领装逼手册，日常生活、出差旅行即刻搞定。终有一天，彪悍人生无须演戏！搜微信公众号：bfaner</p><p><b>每日逼格养成计划请长按此二维码：</b></p><noscript><img src="https://pic4.zhimg.com/c1628e63df28071ad0624affadde85c3_b.jpg" data-rawwidth="258" data-rawheight="258" class="content_image" width="258"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="258" data-rawheight="258" class="content_image lazy" width="258" data-actualsrc="https://pic4.zhimg.com/c1628e63df28071ad0624affadde85c3_b.jpg">', 15, 1, 1458819457, '36e60776bf5d7730fb4936b089d5db2c', '邓潍', '微信公众号“商务范”（微信号：bfaner）', 0)

db_insert(db, sql, params)

db.close()