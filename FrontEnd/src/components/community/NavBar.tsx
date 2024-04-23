import * as n from '@src/components/styles/community/NavbarStyle'
import { useState } from 'react'

const NavBar = () => {
  const [isChoice, setIsChoice] = useState<string>('전체보기')

  const categories = [
    {
      name: '전체보기',
      iconActive: 'src/assets/three_line.svg',
      iconInactive: 'src/assets/three_line_gray.svg',
    },
    {
      name: '이모저모',
      iconActive: 'src/assets/fire.svg',
      iconInactive: 'src/assets/fire_gray.svg',
    },
    {
      name: '인테리어',
      iconActive: 'src/assets/shop.svg',
      iconInactive: 'src/assets/shop_gray.svg',
    },
    {
      name: '상권공유',
      iconActive: 'src/assets/map.svg',
      iconInactive: 'src/assets/map_gray.svg',
    },
    {
      name: '동업제안',
      iconActive: 'src/assets/user_add.svg',
      iconInactive: 'src/assets/user_add_gray.svg',
    },
    {
      name: '창업고민',
      iconActive: 'src/assets/chat.svg',
      iconInactive: 'src/assets/chat_gray.svg',
    },
  ]

  return (
    <n.Container>
      <n.Community>
        <n.Title>커뮤니티</n.Title>
        {categories.map(category => (
          <n.Category
            key={category.name}
            isChoice={isChoice === category.name}
            onClick={() => setIsChoice(category.name)}
          >
            <n.Icon
              src={
                isChoice === category.name
                  ? category.iconActive
                  : category.iconInactive
              }
              alt=""
            />
            <n.Text>{category.name}</n.Text>
          </n.Category>
        ))}
      </n.Community>
      <n.Chatting>
        <n.Title>채팅</n.Title>
      </n.Chatting>
    </n.Container>
  )
}

export default NavBar