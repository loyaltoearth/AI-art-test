import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import Masonry from 'react-masonry-css'

interface Props {
  images: number[]
  titles: { [key: number]: string }
  answers: { [key: number]: string }
  userAnswers: { [key: number]: string }
  imageData: { [key: number]: string }
}

interface State {
  loadedImages: { [key: number]: boolean }
}

class MasonryGrid extends StreamlitComponentBase<State> {
  public state = { loadedImages: {} }
  private gridRef = React.createRef<HTMLDivElement>()
  private resizeObserver: ResizeObserver | null = null

  componentDidMount() {
    this.resizeObserver = new ResizeObserver(entries => {
      for (const entry of entries) {
        Streamlit.setFrameHeight(entry.contentRect.height)
      }
    })

    if (this.gridRef.current) {
      this.resizeObserver.observe(this.gridRef.current)
    }
  }

  componentWillUnmount() {
    if (this.resizeObserver && this.gridRef.current) {
      this.resizeObserver.unobserve(this.gridRef.current)
      this.resizeObserver.disconnect()
    }
  }

  private breakpointColumns = {
    default: 5,
    1400: 4,
    1100: 3,
    700: 2,
    500: 1
  }

  public render = (): ReactNode => {
    const { theme } = this.props
    const { images, titles, answers, userAnswers, imageData } = this.props.args as Props

    const style = {
      '--primary-color': theme?.primaryColor || '#FF4B4B',
      '--text-color': theme?.textColor || '#31333F',
      '--background-color': theme?.backgroundColor || '#FFFFFF',
    } as React.CSSProperties

    return (
      <div style={style} ref={this.gridRef}>
        <style>
          {`
            .masonry-grid {
              display: flex;
              margin-left: -16px;
              width: auto;
            }
            
            .masonry-grid-column {
              padding-left: 16px;
              background-clip: padding-box;
            }

            .masonry-item {
              margin-bottom: 16px;
              break-inside: avoid;
              position: relative;
              border-radius: 8px;
              overflow: hidden;
              box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }

            .image-container {
              position: relative;
            }

            .image-info {
              position: absolute;
              bottom: 0;
              left: 0;
              right: 0;
              background: rgba(0,0,0,0.7);
              color: white;
              padding: 8px 12px;
              font-size: 14px;
              line-height: 1.4;
              display: flex;
              align-items: center;
              gap: 4px;
              white-space: nowrap;
              overflow: hidden;
              text-overflow: ellipsis;
            }

            .title {
              overflow: hidden;
              text-overflow: ellipsis;
            }

            .answer {
              white-space: nowrap;
              margin-left: 4px;
              opacity: 0.9;
            }

            .status-emoji {
              margin-left: 4px;
              font-size: 16px;
            }

            img {
              width: 100%;
              height: auto;
              display: block;
            }

            ::-webkit-scrollbar {
              display: none;
            }
            
            * {
              -ms-overflow-style: none;
              scrollbar-width: none;
            }
          `}
        </style>
        
        <Masonry
          breakpointCols={this.breakpointColumns}
          className="masonry-grid"
          columnClassName="masonry-grid-column"
        >
          {images.map((imgNum) => (
            <div key={imgNum} className="masonry-item">
              <div className="image-container">
                <img
                  src={`data:image/png;base64,${imageData[imgNum]}`}
                  alt={titles[imgNum]}
                  onLoad={(e) => this.handleImageLoad(imgNum, e)}
                />
                <div className="image-info">
                  <span className="title">{titles[imgNum]}</span>
                  <span className="answer">({answers[imgNum].toUpperCase()})</span>
                  <span className="status-emoji">
                    {answers[imgNum].toUpperCase() === userAnswers[imgNum]?.toUpperCase() ? '✅' : '❌'}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </Masonry>
      </div>
    )
  }

  private handleImageLoad = (imgNum: number, event: React.SyntheticEvent<HTMLImageElement>): void => {
    this.setState(prevState => ({
      loadedImages: {
        ...prevState.loadedImages,
        [imgNum]: true
      }
    }), () => {
      if (this.gridRef.current) {
        Streamlit.setFrameHeight(this.gridRef.current.scrollHeight)
      }
    })
  }
}

export default withStreamlitConnection(MasonryGrid)