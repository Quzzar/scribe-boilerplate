import { Flex, Image, Text } from '@mantine/core';
import LogoImg from '../../assets/logo.svg';

export function LogoFull(props: { size?: number }) {

  return (
    <Flex
      wrap="nowrap"
      onClick={() => {
        window.location.href = '/';
      }}
      py='xs'
      className="cursor-pointer"
      sx={{ userSelect: 'none', position: 'relative' }}
    >
      <Image
        height={props.size || 26}
        fit="contain"
        src={LogoImg}
        alt="SellScale Scribe"
      />
      <Text
        size={28}
        color='#fff'
        ff={"'Caveat', cursive"}
        sx={{ position: 'absolute', top: 2, right: -63 }}
      >Scribe</Text>
    </Flex>
  );
}