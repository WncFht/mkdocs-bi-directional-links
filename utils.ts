import type MarkdownIt from 'markdown-it'
import type StateInline from 'markdown-it/lib/rules_inline/state_inline.mjs'
import { sep } from 'node:path'
import Token from 'markdown-it/lib/token.mjs'

const caseInsensitiveCompare = new Intl.Collator(undefined, { sensitivity: 'accent' }).compare

export function findBiDirectionalLinks(
    possibleBiDirectionalLinksInFilePaths: Record<string, string>,
    possibleBiDirectionalLinksInFullFilePaths: Record<string, string>,
    href: string,
  ): string[] | string | null {
    if (!href)
      return null
  
    if (href.includes(sep))
      return possibleBiDirectionalLinksInFullFilePaths[href] ?? Object.entries(possibleBiDirectionalLinksInFullFilePaths).filter(p => caseInsensitiveCompare(href, p[0]) === 0).map(p => p[1])
  
    return possibleBiDirectionalLinksInFilePaths[href] ?? Object.entries(possibleBiDirectionalLinksInFilePaths).filter(p => caseInsensitiveCompare(href, p[0]) === 0).map(p => p[1])
  }

  export function genLink(
    state: StateInline,
    resolvedNewHref: string,
    text: string,
    md: MarkdownIt,
    href: string,
    link: RegExpMatchArray,
  ) {
    // 创建 link_open Token
    const openToken = state.push('link_open', 'a', 1)
    openToken.attrSet('href', resolvedNewHref)
  
    // 用于存储链接内容的子 Token
    const linkTokenChildrenContent: Token[] = []
  
    // 移除 href 中的查询参数和哈希
    const parsedUrl = new URL(href, 'https://a.com')
    const hrefWithoutSearchAndHash = decodeURIComponent(parsedUrl.pathname.slice(1))
  
    // 解析文本内容为 inline Token
    const parsedInlineTokens = text
      ? md.parseInline(text, state.env)
      : md.parseInline(hrefWithoutSearchAndHash, state.env) || []
  
    // 将解析后的子 Token 添加到 linkTokenChildrenContent
    if (parsedInlineTokens && parsedInlineTokens.length) {
      parsedInlineTokens.forEach((tokens) => {
        if (!tokens.children)
          return
  
        tokens.children.forEach((token) => {
          linkTokenChildrenContent.push(token)
        })
      })
    }
  
    // 将子 Token 推入 state
    for (const token of linkTokenChildrenContent) {
      const pushedToken = state.push(token.type, token.tag, token.nesting)
      pushedToken.content = token.content
    }
  
    // 创建 link_close Token
    state.push('link_close', 'a', -1)
  
    // 更新 state 中的位置
    state.pos += link![0].length
  }

  export function genImage(
    state: StateInline,
    resolvedNewHref: string,
    text: string,
    link: RegExpMatchArray,
  ) {
    const openToken = state.push('image', 'img', 1)
    openToken.attrSet('src', resolvedNewHref)
    openToken.attrSet('alt', '')
  
    openToken.children = []
    openToken.content = text
  
    const innerTextToken = new Token('text', '', 0)
    innerTextToken.content = text
    openToken.children.push(innerTextToken)
  
    state.pos += link![0].length
  }

  export function genVideo(
    state: StateInline,
    resolvedNewHref: string,
    text: string,
    link: RegExpMatchArray,
  ) {
    const openToken = state.push('video_open', 'video', 1)
    openToken.attrSet('controls', 'true')
    openToken.attrSet('preload', 'metadata')
    if (text)
      openToken.attrSet('aria-label', text)
  
    const sourceOpenToken = state.push('source_open', 'source', 1)
    sourceOpenToken.attrSet('src', resolvedNewHref)
  
    state.push('video_close', 'video', -1)
  
    state.pos += link![0].length
  }

  export function genAudio(
    state: StateInline,
    resolvedNewHref: string,
    text: string,
    link: RegExpMatchArray,
  ) {
    const openToken = state.push('audio_open', 'audio', 1)
    openToken.attrSet('controls', 'true')
    openToken.attrSet('preload', 'metadata')
    if (text)
      openToken.attrSet('aria-label', text)
  
    const sourceOpenToken = state.push('source_open', 'source', 1)
    sourceOpenToken.attrSet('src', resolvedNewHref)
  
    state.push('audio_close', 'audio', -1)
  
    state.pos += link![0].length
  }

