import styled, { keyframes } from 'styled-components'

const mulShdSpin = keyframes`
    0%,
    100% {
        box-shadow:
                0em -2.6em 0em 0em #5057ff,
                1.8em -1.8em 0 0em rgba(0, 102, 255, 0.2),
                2.5em 0em 0 0em rgba(0, 102, 255, 0.2),
                1.75em 1.75em 0 0em rgba(0, 102, 255, 0.2),
                0em 2.5em 0 0em rgba(0, 102, 255, 0.2),
                -1.8em 1.8em 0 0em rgba(0, 102, 255, 0.2),
                -2.6em 0em 0 0em rgba(0, 102, 255, 0.5),
                -1.8em -1.8em 0 0em rgba(255, 255, 255, 0.7);
    }
    12.5% {
        box-shadow:
                0em -2.6em 0em 0em rgba(0, 102, 255, 0.7),
                1.8em -1.8em 0 0em #5057ff,
                2.5em 0em 0 0em rgba(0, 102, 255, 0.2),
                1.75em 1.75em 0 0em rgba(0, 102, 255, 0.2),
                0em 2.5em 0 0em rgba(0, 102, 255, 0.2),
                -1.8em 1.8em 0 0em rgba(0, 102, 255, 0.2),
                -2.6em 0em 0 0em rgba(0, 102, 255, 0.2),
                -1.8em -1.8em 0 0em rgba(0, 102, 255, 0.5);
    }
    25% {
        box-shadow:
                0em -2.6em 0em 0em rgba(0, 102, 255, 0.5),
                1.8em -1.8em 0 0em rgba(0, 102, 255, 0.7),
                2.5em 0em 0 0em #5057ff,
                1.75em 1.75em 0 0em rgba(0, 102, 255, 0.2),
                0em 2.5em 0 0em rgba(0, 102, 255, 0.2),
                -1.8em 1.8em 0 0em rgba(0, 102, 255, 0.2),
                -2.6em 0em 0 0em rgba(0, 102, 255, 0.2),
                -1.8em -1.8em 0 0em rgba(0, 102, 255, 0.2);
    }
    37.5% {
        box-shadow:
                0em -2.6em 0em 0em rgba(0, 102, 255, 0.2),
                1.8em -1.8em 0 0em rgba(0, 102, 255, 0.5),
                2.5em 0em 0 0em rgba(0, 102, 255, 0.7),
                1.75em 1.75em 0 0em #5057ff,
                0em 2.5em 0 0em rgba(0, 102, 255, 0.2),
                -1.8em 1.8em 0 0em rgba(0, 102, 255, 0.2),
                -2.6em 0em 0 0em rgba(0, 102, 255, 0.2),
                -1.8em -1.8em 0 0em rgba(0, 102, 255, 0.2);
    }
    50% {
        box-shadow:
                0em -2.6em 0em 0em rgba(0, 102, 255, 0.2),
                1.8em -1.8em 0 0em rgba(0, 102, 255, 0.2),
                2.5em 0em 0 0em rgba(0, 102, 255, 0.5),
                1.75em 1.75em 0 0em rgba(0, 102, 255, 0.7),
                0em 2.5em 0 0em #5057ff,
                -1.8em 1.8em 0 0em rgba(0, 102, 255, 0.2),
                -2.6em 0em 0 0em rgba(0, 102, 255, 0.2),
                -1.8em -1.8em 0 0em rgba(0, 102, 255, 0.2);
    }
    62.5% {
        box-shadow:
                0em -2.6em 0em 0em rgba(0, 102, 255, 0.2),
                1.8em -1.8em 0 0em rgba(0, 102, 255, 0.2),
                2.5em 0em 0 0em rgba(0, 102, 255, 0.2),
                1.75em 1.75em 0 0em rgba(0, 102, 255, 0.5),
                0em 2.5em 0 0em rgba(0, 102, 255, 0.7),
                -1.8em 1.8em 0 0em #5057ff,
                -2.6em 0em 0 0em rgba(0, 102, 255, 0.2),
                -1.8em -1.8em 0 0em rgba(0, 102, 255, 0.2);
    }
    75% {
        box-shadow:
                0em -2.6em 0em 0em rgba(0, 102, 255, 0.2),
                1.8em -1.8em 0 0em rgba(0, 102, 255, 0.2),
                2.5em 0em 0 0em rgba(0, 102, 255, 0.2),
                1.75em 1.75em 0 0em rgba(0, 102, 255, 0.2),
                0em 2.5em 0 0em rgba(0, 102, 255, 0.5),
                -1.8em 1.8em 0 0em rgba(0, 102, 255, 0.7),
                -2.6em 0em 0 0em #5057ff,
                -1.8em -1.8em 0 0em rgba(0, 102, 255, 0.2);
    }
    87.5% {
        box-shadow:
                0em -2.6em 0em 0em rgba(0, 102, 255, 0.2),
                1.8em -1.8em 0 0em rgba(0, 102, 255, 0.2),
                2.5em 0em 0 0em rgba(0, 102, 255, 0.2),
                1.75em 1.75em 0 0em rgba(0, 102, 255, 0.2),
                0em 2.5em 0 0em rgba(0, 102, 255, 0.2),
                -1.8em 1.8em 0 0em rgba(0, 102, 255, 0.5),
                -2.6em 0em 0 0em rgba(0, 102, 255, 0.7),
                -1.8em -1.8em 0 0em #5057ff;
    }
`

const LoadingSpinner = styled.div`
  font-size: 10px;
  width: 1em;
  height: 1em;
  border-radius: 50%;
  position: relative;
  text-indent: -9999em;
  animation: ${mulShdSpin} 1.1s infinite ease;
  transform: translateZ(0);
`

const CircleLoading = () => {
  return <LoadingSpinner />
}

export default CircleLoading
